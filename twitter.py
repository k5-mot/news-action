import requests
import os
import json
import datetime

bearer_token = os.environ.get("BEARER_TOKEN")
discord_webhook = os.environ.get("DISCORD_WEBHOOK")


def get_user_lookup(username):
    '''
    ユーザ名からユーザIDを取得
    '''
    usernames = "usernames={}".format(username)
    user_fields = "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }
    response = requests.request("GET", url, headers=headers,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user_tweets(user_id):
    '''
    ユーザIDからユーザの最新ツイートを取得
    '''
    url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserTweetsPython"
    }
    params = {
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld",
        "expansions": "attachments.media_keys",
        "media.fields": "media_key,type,duration_ms,height,url,width,alt_text"
    }
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def convert_to_datetime(datetime_str):
    tweet_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    jst_datetime = tweet_datetime.astimezone(datetime.timezone(datetime.timedelta(hours=+9), 'JST'))
    return jst_datetime


def notify_discord(lookup, tweets):
    '''
    最新ツイートをDiscordに転送
    '''
    url = "https://twitter.com/" + lookup['data'][0]['username'] + "/status/" + lookup['data'][0]['id']
    json_send = {
        "username": lookup['data'][0]['name'],
        "avatar_url": lookup['data'][0]['profile_image_url'],
        "embeds": [
            {
                "color": 1942002,
                "author": {
                    "name": lookup['data'][0]['name'] + " (@" + lookup['data'][0]['username'] + ")",
                    "url": "https://twitter.com/" + lookup['data'][0]['username'],
                    "icon_url": lookup['data'][0]['profile_image_url']
                },
                "url": url,
                "description": tweets['data'][0]['text'],
                "footer": {
                    "text": tweets['data'][0]['source'],
                    "icon_url": "https://abs.twimg.com/icons/apple-touch-icon-192x192.png"
                },
                "timestamp": tweets['data'][0]['created_at']
            }
        ]
    }

    first = True
    if 'attachments' in tweets['data'][0]:
        for img_key in tweets['data'][0]['attachments']['media_keys']:
            for media in tweets['includes']['media']:
                if img_key == media['media_key']:
                    imgurl = media['url']
                    break
            if first:
                first = False
                json_send['embeds'][0]['image'] = {}
                json_send['embeds'][0]['image']['url'] = imgurl
            else:
                part_json = {
                    "image": {
                        "url": imgurl
                    },
                    "url": url
                }
                json_send['embeds'].append(part_json)

    response = requests.post(discord_webhook, json.dumps(json_send), headers={'Content-Type': 'application/json'})
    print(json_send)
    print(response.status_code)


def main():
    usernames = ['NU_kouhou', 'nu_idsci', 'ShigeruKohno', 'nagasakicareer', 'nuc_bunkyo_shop', 'nuc_univ_coop', 'NagasakiUniLib']
    for username in usernames:
        user_lookup = get_user_lookup(username)
        print(json.dumps(user_lookup, indent=4, sort_keys=True, ensure_ascii=False))
        user_tweets = get_user_tweets(int(user_lookup['data'][0]['id']))
        print(json.dumps(user_tweets, indent=4, sort_keys=True, ensure_ascii=False))

        post_time = convert_to_datetime(user_tweets['data'][0]['created_at'])
        now_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+9), 'JST'))
        updatetime = now_time - datetime.timedelta(minutes=30)
        if updatetime < post_time:
            notify_discord(user_lookup, user_tweets)
            print(user_tweets['data'][0]['text'])


if __name__ == "__main__":
    main()
