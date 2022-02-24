from __future__ import print_function
import sys
import os
import datetime
import requests
import json
from bs4 import BeautifulSoup
import feedparser
import pickle
import difflib
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError


def get_news():
    # List of News source
    RSS_URLS = [
        # My navi
        'https://news.mynavi.jp/rss/index',
        'https://news.mynavi.jp/rss/techplus/enterprise/itsystem',
        'https://news.mynavi.jp/rss/techplus/enterprise/mobilesolution',
        'https://news.mynavi.jp/rss/techplus/enterprise/management',
        'https://news.mynavi.jp/rss/techplus/enterprise/educationit',
        'https://news.mynavi.jp/rss/techplus/enterprise/marketing',
        'https://news.mynavi.jp/rss/techplus/enterprise/vendor_contents',
        'https://news.mynavi.jp/rss/techplus/enterprise/security',
        'https://news.mynavi.jp/rss/techplus/enterprise/engineer',
        'https://news.mynavi.jp/rss/techplus/enterprise/soho',
        'https://news.mynavi.jp/rss/techplus/enterprise/corp',
        'https://news.mynavi.jp/rss/techplus/enterprise/bizskillup',
        'https://news.mynavi.jp/rss/techplus/technology/semiconductor',
        'https://news.mynavi.jp/rss/techplus/technology/carelectronics',
        'https://news.mynavi.jp/rss/techplus/technology/embedded',
        'https://news.mynavi.jp/rss/techplus/technology/measurement',
        'https://news.mynavi.jp/rss/techplus/technology/medical',
        'https://news.mynavi.jp/rss/techplus/technology/aerospace',
        'https://news.mynavi.jp/rss/techplus/technology/future_tech',
        'https://news.mynavi.jp/rss/techplus/technology/rt',
        'https://news.mynavi.jp/rss/techplus/technology/sc',
        'https://news.mynavi.jp/rss/techplus/technology/energy',
        'https://news.mynavi.jp/rss/techplus/technology/science',
        'https://news.mynavi.jp/rss/techplus/technology/monozukuri',
        'https://news.mynavi.jp/rss/digital/pc/windows',
        'https://news.mynavi.jp/rss/digital/pc/hontai',
        'https://news.mynavi.jp/rss/digital/pc/peripheral',
        'https://news.mynavi.jp/rss/digital/pc/software',
        'https://news.mynavi.jp/rss/digital/pc/pcsecurity',
        'https://news.mynavi.jp/rss/digital/pc/apple',
        'https://news.mynavi.jp/rss/digital/pc/pc_gaming',
        'https://news.mynavi.jp/rss/digital/pc/jisaku',
        'https://news.mynavi.jp/rss/digital/pc/internet',
        'https://news.mynavi.jp/rss/digital/pc/pccampaign',
        # GIGAZINE
        'https://gigazine.net/news/rss_2.0/',
        # Lifehacker
        'https://www.lifehacker.jp/feed/index.xml',
        # SUNDAY
        'https://yukawanet.com/feed',
        'https://yukawanet.com/comments/feed',
        # J-CAST
        'https://www.j-cast.com/atom.xml',
        'https://www.j-cast.com/tv/atom.xml',
        'https://www.j-cast.com/trend/atom.xml',
        'https://www.j-cast.com/kaisha/atom.xml',
        # ITmedia
        'https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml',
        'https://rss.itmedia.co.jp/rss/2.0/topstory.xml',
        'https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml',
        'https://rss.itmedia.co.jp/rss/2.0/news_domestic.xml',
        'https://rss.itmedia.co.jp/rss/2.0/news_foreign.xml',
        'https://rss.itmedia.co.jp/rss/2.0/mobile.xml',
        'https://rss.itmedia.co.jp/rss/2.0/pcuser.xml',
        'https://rss.itmedia.co.jp/rss/2.0/business.xml',
        'https://rss.itmedia.co.jp/rss/2.0/enterprise.xml',
        'https://rss.itmedia.co.jp/rss/2.0/executive.xml',
        'https://rss.itmedia.co.jp/rss/2.0/marketing.xml',
        # 調査のチカラ
        'https://chosa.itmedia.co.jp/recent.xml',
        # @IT
        'https://rss.itmedia.co.jp/rss/2.0/ait.xml',
        # キーマンズネット
        'https://rss.itmedia.co.jp/rss/2.0/keymans.xml',
        # Techtarget
        'https://rss.itmedia.co.jp/rss/2.0/techtarget.xml',
        # MONOist
        'https://rss.itmedia.co.jp/rss/2.0/monoist.xml',
        # EE Times Japan
        'https://rss.itmedia.co.jp/rss/2.0/eetimes.xml',
        # EDN Japan
        'https://rss.itmedia.co.jp/rss/2.0/edn.xml',
        # Smart Japan
        'https://rss.itmedia.co.jp/rss/2.0/smartjapan.xml',
        # BUILT
        'https://rss.itmedia.co.jp/rss/2.0/sj_built.xml',
        # TechTarget
        'https://rss.itmedia.co.jp/rss/2.0/techfactory.xml',
        # Netlab
        'https://rss.itmedia.co.jp/rss/2.0/netlab.xml',
        # Engadget
        'http://www.engadget.com/rss.xml',
        'https://japanese.engadget.com/rss.xml',
        # Impress Watch
        'https://www.watch.impress.co.jp/data/rss/1.0/ipw/feed.rdf',
        # INTERNET Watch
        'https://internet.watch.impress.co.jp/data/rss/1.0/iw/feed.rdf',
        # PC Watch
        'https://pc.watch.impress.co.jp/data/rss/1.0/pcw/feed.rdf',
        # デジカメ Watch
        'https://dc.watch.impress.co.jp/data/rss/1.0/dcw/feed.rdf',
        # AKIBA PC Hotline!
        'https://akiba-pc.watch.impress.co.jp/data/rss/1.0/ah/feed.rdf',
        # AV Watch
        'https://av.watch.impress.co.jp/data/rss/1.0/avw/feed.rdf',
        # 家電 Watch
        'https://kaden.watch.impress.co.jp/data/rss/1.0/kdw/feed.rdf',
        # ケータイ Watch
        'https://k-tai.watch.impress.co.jp/data/rss/1.0/ktw/feed.rdf',
        # クラウド Watch
        'https://cloud.watch.impress.co.jp/data/rss/1.0/clw/feed.rdf',
        # Watch Video
        'https://video.watch.impress.co.jp/data/rss/1.0/video/feed.rdf',
        # 窓の杜
        'https://forest.watch.impress.co.jp/data/rss/1.0/wf/feed.rdf',
        # こどもとIT
        'https://edu.watch.impress.co.jp/data/rss/1.0/kit/feed.rdf',
        # Car Watch
        'https://car.watch.impress.co.jp/data/rss/1.0/car/feed.rdf',
        # トラベル Watch
        'http://travel.watch.impress.co.jp/docs/travel.rdf',
        # グルメ Watch
        'https://gourmet.watch.impress.co.jp/data/rss/1.0/grw/feed.rdf',
        # GAME Watch
        'https://game.watch.impress.co.jp/data/rss/1.0/gmw/feed.rdf',
        # HOBBY Watch
        'https://hobby.watch.impress.co.jp/data/rss/1.0/hbw/feed.rdf',
        # Wired
        'https://www.wired.com/feed/rss',
        # Wired.jp
        'https://feeds.dailyfeed.jp/feed/s/22/348.rss',
        # GIZMODO
        'https://www.gizmodo.jp/index.xml',
        # 'https://gizmodo.com/rss',
        # 日経ビジネス
        'https://business.nikkei.com/rss/all_nb.rdf',
        # 日経クロステック
        'https://tech.nikkeibp.co.jp/rss/index.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-it.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-dm.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-ele.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-mono.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-at.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-ene.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-hlth.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-bld.rdf',
        'https://tech.nikkeibp.co.jp/rss/xtech-con.rdf',
        # 東洋経済オンライン
        'https://toyokeizai.net/list/feed/rss',
        # 市況かぶ全力２階建
        'https://kabumatome.doorblog.jp/atom.xml',
        # 帝国データバンク
        'https://www.tdb.co.jp/rss/jouhou.rdf',
        # ACRi
        'https://www.acri.c.titech.ac.jp/wordpress/feed',
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCL15_5A9JKcVrmFUcMto6-Q',
        # PR TIMES
        'https://prtimes.jp/index.rdf',
        # ZDNet Japan
        'http://feeds.japan.zdnet.com/rss/zdnet/all.rdf',
        # Dream News
        'https://www.dreamnews.jp/?action_rss=1',
        # ZNews Africa
        # 'https://znewsafrica.com/feed/',
        # The Next Platform
        # 'https://www.nextplatform.com/feed/',
        # Design & Reuse
        # 'https://www.design-reuse.com/xml/1/1/all/rss.xml',
        # 'https://www.design-reuse.com/xml/1/1/news/rss.xml',
        # All About Circuits
        # 'http://www.allaboutcircuits.com/rss/',
        # HACKADAY
        # 'https://hackaday.com/feed/',
        # ASCII.jp
        'https://ascii.jp/rss.xml',
        'https://ascii.jp/biz/rss.xml',
        'https://ascii.jp/tech/rss.xml',
        'https://ascii.jp/web/rss.xml',
        # 'https://ascii.jp/digital/rss.xml',
        'https://ascii.jp/mac/rss.xml',
        'https://ascii.jp/hobby/rss.xml',
        'https://ascii.jp/pc/rss.xml',
        # ロボスタ
        'https://robotstart.info/feed',
        # テクノプロ
        'https://www.technopro.com/feed',
        # 現代ビジネス
        'https://gendai.ismedia.jp/list/feed/rss',
        # Bloomberg
        'https://about.bloomberg.co.jp/feed',
        # 'https://www.bloomberg.com/professional/feed/',
        # ダイヤモンド・オンライン
        'https://diamond.jp/list/feed/rss/dol',
        # Business Journal
        'https://biz-journal.jp/index.xml',
        # PRESIDENT Online
        'https://president.jp/list/rss',
        # Publickey
        'https://www.publickey1.jp/atom.xml',
        # 不景気.com
        'https://www.fukeiki.com/atom.xml',
        # Newsweek
        'https://www.newsweekjapan.jp/story/rss.xml',
        # AUTOMATON
        'https://automaton-media.com/feed/',
        # PCパーツまとめ
        # 'http://blog.livedoor.jp/bluejay01-review/atom.xml',
        # スラド
        'http://srad.jp/sradjp.rss',
        # 徳丸浩の日記 (セキュリティ)
        'https://blog.tokumaru.org/',
        # Web Creator Box
        'https://www.webcreatorbox.com/',
        # コリス
        'http://coliss.com/feed/',
        # FPGAの部屋
        'https://marsee101.blog.fc2.com/?xml',
        # FPGA開発日記
        'https://msyksphinz.hatenablog.com/feed',
        # FPGA Developer
        'https://www.fpgadeveloper.com/index.xml',
        # ハートランド・ザ・ワールド
        'https://hldc.co.jp/blog/feed/',
        # FPGAの部屋まとめ
        'http://fpga.blog.jp/atom.xml',
        # GMO
        'https://recruit.gmo.jp/engineer/jisedai/blog/feed/',
        # Sparkfun
        # 'https://www.sparkfun.com/feeds/news',
        # 'https://www.sparkfun.com/feeds/products',
        # Dangerous Prototypes
        # 'http://dangerousprototypes.com/blog/feed/',
        # Analog Devices
        # 'https://ez.analog.com/rss',
        # Achronix
        # 'https://www.achronix.com/rss.xml',
        # Plunify
        # 'https://support.plunify.com/en/feed/',
        # Digitronix Nepal
        # 'https://www.youtube.com/feeds/videos.xml?channel_id=UCfd9WcJUGiNggdU5BXvvvZg',
        # FPGA4Student
        # 'https://www.fpga4student.com/feeds/posts/default',
        # FPGA Releated Blog
        # 'https://www.fpgarelated.com/blogs_rss.php',
        # Intel FPGA
        'https://www.youtube.com/feeds/videos.xml?user=alteracorp',
        # Xilinx
        'https://www.youtube.com/feeds/videos.xml?user=XilinxInc',
        # FPGA Coding
        # 'https://fpgacoding.com/feed/',
        # Exostiv Labs
        # 'https://www.exostivlabs.com/feed/',
        # Annapolis Micro Systems
        # 'https://www.annapmicro.com/feed/',
        # ZipCPU
        # 'https://zipcpu.com/feed.xml',
        # Aldec
        # 'https://www.aldec.com/rss',
        # Digilent
        'https://digilent.com/blog/feed/',
        # SEO Japan
        'https://www.seojapan.com/blog/feed',
        # Macnica
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCMm9NUzYr4zGWMDllZ2Rghg',
        # NTT DATA
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCAqNtQC0e1eBrwIBpVmZung',
        # Digi-Key
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCclJCqMDAkyVGsm5oFOTXIQ',
        # 海外SEO情報ブログ
        # 'https://www.suzukikenichi.com/blog/feed/',
        # 'https://www.suzukikenichi.com/blog/web-stories/feed/',
        # そうさめも
        # 'http://miki800.com/feed/',
        # ゲームカタログ@Wiki ～名作からクソゲーまで～
        'http://w.atwiki.jp/gcmatome/feed.atom',
        # Makuake
        'https://www.makuake.com/atom/',
        # 280blocker
        'https://280blocker.net/feed/',
        # STUDY HACKER
        'https://studyhacker.net/feed',
        # Chrome Releases
        'https://chromereleases.googleblog.com/feeds/posts/default',
        # AWS
        'https://aws.amazon.com/rss',
        # Mozilla Blog
        'https://blog.mozilla.org/en/feed/',
        # Dwango
        'http://creator.dwango.co.jp/feed/rss',
        # KDII
        'http://cloudblog.kddi.com/feed/',
        # NTT
        'https://engineers.ntt.com/feed',
        # Yahoo! JAPAN
        'https://techblog.yahoo.co.jp/atom.xml',
        # CyberAgent
        'https://developers.cyberagent.co.jp/blog/feed/',
        # Yahoo! News
        'https://news.yahoo.co.jp/rss/topics/it.xml',
        'https://news.yahoo.co.jp/rss/categories/it.xml',
    ]

    # Search keywords
    keywords = [
        'Xilinx', 'Altera', 'FPGA', 'Intel', 'AMD', 'NVIDIA',
        'Field-Programmable Gate Array', 'HDL', 'HLS', 'Arm',
        'Field Programmable Gate Array', 'ASIC', 'CPU', 'GPU', 'CUDA',
        'Sony', 'Semiconductor', 'セミコンダクタ', 'terastic', '半導体',
        'Lattice', 'MicroSemi', 'Verilog', 'SystemVerilog',
        'Verilog-HDL', 'HDL', 'ASIC',
        'Digilent', 'Avnet', 'Quartus', 'Vivado', 'Vitis', 'SystemC',
        '富岳', '富嶽',
    ]

    # Collect latest news
    print('Collecting latest news...')
    # print(keywords)
    news_list = set()
    for RSS_URL in RSS_URLS:
        # print(RSS_URL)
        d = feedparser.parse(RSS_URL)
        for entry in d.entries:

            # Get published date
            pdate = None
            if entry.has_key('published'):
                pdate = entry.published_parsed
            elif entry.has_key('updated'):
                pdate = entry.updated_parsed
            elif entry.has_key('created'):
                pdate = entry.created_parsed
            elif entry.has_key('expired'):
                pdate = entry.expired_parsed

            # Is exist date
            if pdate is None:
                continue

            # Judge latest news
            pdate = datetime.datetime(*pdate[:6], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            jst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            if pdate < (jst_time + datetime.timedelta(days=-1)):
                continue

            # Compare news list
            cflg = False
            for newsline in news_list:
                samer = difflib.SequenceMatcher(None, newsline[1], entry.title).ratio()
                if 0.85 < samer:
                    cflg = True
                    break
            if cflg:
                continue

            # Search keywords
            for keyword in keywords:
                if keyword in entry.title:
                    # print(pdate, keyword, entry.title, entry.link)
                    news_list.add(tuple([pdate, entry.title, entry.link]))
                    break

    # Print all latest news
    print('Print latest news')
    for news in news_list:
        print(news[0], news[1], news[2])

    cns = []
    for news in news_list:
        htmldata = requests.get(news[2]).text
        soup = BeautifulSoup(htmldata, 'html.parser')
        mainimg = soup.find('meta', attrs={'property': 'og:image', 'content': True})
        imgsrc = None
        if mainimg is not None:
            imgsrc = mainimg['content']
            cn = {
                "title": news[1],
                "url": news[2],
                "color": 1752220,
                "thumbnail": {
                    "url": imgsrc
                }
            }
            cns.append(cn)
    return cns


def get_weather():
    print('Make embeds of weather broadcasts')
    city_name = "Nagasaki"
    API_KEY = sys.argv[2]
    api = "http://api.openweathermap.org/data/2.5/weather?units=metric&lang=ja&q={city}&appid={key}"
    url = api.format(city=city_name, key=API_KEY)
    response = requests.get(url)
    data = response.json()
    jsonText = json.dumps(data, indent=4)
    print(jsonText)
    # print(data)
    cn = {
        "title": data['name'] + "の天気",
        "description": datetime.datetime.fromtimestamp(data['dt']).strftime('%Y/%m/%d (%a)'),
        "url": "https://openweathermap.org/city/1856177",
        "color": 5620992,
        "image": {
        #     "url": "https://pbs.twimg.com/profile_banners/1159383628951851008/1565318066/1500x500",
            "url": "https://source.unsplash.com/uj7eb7CgqRk/1080x300",
        },
        "thumbnail": {
            "url": "http://openweathermap.org/img/w/" + data['weather'][0]['icon'] + ".png"
        },
        "fields": [
            {
                "name": "天気",
                "value": data['weather'][0]['description'],
            },
            {
                "name": "気温",
                "value": str(data['main']['temp']) + " [℃]",
                "inline": True
            },
            {
                "name": "最高気温",
                "value": str(data['main']['temp_max']) + " [℃]",
                "inline": True
            },
            {
                "name": "最低気温",
                "value": str(data['main']['temp_min']) + " [℃]",
                "inline": True
            },
            {
                "name": "湿度",
                "value": str(data['main']['humidity']) + " [%]",
                "inline": True
            },
            {
                "name": "日出",
                "value": datetime.datetime.fromtimestamp(data['sys']['sunrise'], tz=datetime.timezone(datetime.timedelta(hours=9))).strftime('%H:%M'),
                "inline": True
            },
            {
                "name": "日没",
                "value": datetime.datetime.fromtimestamp(data['sys']['sunset'], tz=datetime.timezone(datetime.timedelta(hours=9))).strftime('%H:%M'),
                "inline": True
            },
            {
                "name": "気圧",
                "value": str(data['main']['pressure']) + " [hPa]",
                "inline": True
            },
            {
                "name": "風速",
                "value": str(data['wind']['speed']) + ' [m/s]',
                "inline": True
            },
            {
                "name": "風向",
                "value": str(data['wind']['deg']) + ' [°]',
                "inline": True
            },
            {
                "name": "経度",
                "value": str(data['coord']['lon']) + ' [°]',
                "inline": True
            },
            {
                "name": "緯度",
                "value": str(data['coord']['lat']) + ' [°]',
                "inline": True
            },
            {
                "name": "国",
                "value": str(data['sys']['country']),
                "inline": True
            },
        ]
    }
    return cn


# def get_calender():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     # If modifying these scopes, delete the file token.json.
#     SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#
#     try:
#         service = build('calendar', 'v3', credentials=creds)
#
#         # Call the Calendar API
#         now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC Time
#         print('Getting the upcoming 10 events')
#         events_result = service.events().list(calendarId='primary', timeMin=now,
#                                               maxResults=10, singleEvents=True,
#                                               orderBy='startTime').execute()
#         events = events_result.get('items', [])
#
#         cn = {
#             "title": "今日の予定",
#             #"url": news[2],
#             "description": datetime.datetime.now().strftime('%Y/%m/%d (%a)'),
#             "color": 16776960,
#             "thumbnail": {
#                 "url": "https://avatars.githubusercontent.com/u/34744243?v=4"
#             },
#             "fields": []
#         }
#
#         if not events:
#             print('No upcoming events found.')
#             return
#
#         # Prints the start and name of the next 10 events
#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             print(start, event['summary'])
#             goal = {
#                 "name": start,
#                 "value": event['summary']
#             }
#             cn['fields'].append(goal)
#
#         return cn
#
#     except HttpError as error:
#         print('An error occurred: %s' % error)


def main():
    print('Make embeds of news list')
    webhook_url = sys.argv[1]
    main_content = {
        "username": "NEWS Bot",
        "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    }
    main_content["embeds"] = []
    main_content["embeds"] = get_news()
    main_content["embeds"].append(get_weather())
    # main_content["embeds"].append(get_calender())

    # News & weather
    print('Notification of News & WEather')
    print(main_content)
    res = requests.post(webhook_url, json.dumps(main_content), headers={'Content-Type': 'application/json'})
    print(res)
    # print(main_content)


if __name__ == '__main__':
    main()
