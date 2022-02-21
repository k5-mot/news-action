import sys
import datetime
import requests
import json
from bs4 import BeautifulSoup
import feedparser


def getdata(url):
  r = requests.get(url)
  return r.text


def main():
  # List of News source
  RSS_URLS = [
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
    'https://news.mynavi.jp/rss/techplus/enterprise/bizskillup'
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
    'https://news.yahoo.co.jp/rss/topics/it.xml',
    'https://news.yahoo.co.jp/rss/categories/it.xml',
    'https://pc.watch.impress.co.jp/data/rss/1.0/pcw/feed.rdf',
    'https://rss.itmedia.co.jp/rss/2.0/monoist.xml',
    'https://rss.itmedia.co.jp/rss/2.0/techfactory.xml',
    'https://wp.techfactory.itmedia.co.jp/dcparts/tf/2.0/m0.xml',
    'https://rss.itmedia.co.jp/rss/2.0/eetimes.xml',
    'https://prtimes.jp/index.rdf',
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
    'https://it.impress.co.jp/list/feed/rss',
    'https://car.watch.impress.co.jp/data/rss/1.0/car/feed.rdf',
    'https://ascii.jp/rss.xml',
    'https://av.watch.impress.co.jp/data/rss/1.0/avw/feed.rdf',
    'https://gigazine.net/news/rss_2.0/',
    'https://aws.amazon.com/rss',
    'https://robotstart.info/feed',
    'https://www.technopro.com/feed',
    'https://www.acri.c.titech.ac.jp/wordpress/feed',
  ]

  # Search keywords
  keywords = [
    'Xilinx', 'Altera', 'FPGA', 'Intel', 'AMD', 'NVIDIA',
    'Field-Programmable Gate Array', 'HDL', 'HLS', 'Arm',
    'Field Programmable Gate Array', 'ASIC', '半導体',
    'Sony', 'Semiconductor', 'セミコンダクタ', 'terastic',
    'Lattice', 'MicroSemi', 'Verilog', 'SystemVerilog',
    'Digilent', 'Avnet', 'Quartus', 'Vivado', 'Vitis', 'SystemC'
  ]

  # Collect latest news
  news_list = set()
  for RSS_URL in RSS_URLS:
    d = feedparser.parse(RSS_URL)
    for entry in d.entries:
      # Search keywords
      for keyword in keywords:
        if keyword in entry.title:
          # Get date written
          if entry.has_key('published'):
            pdate = entry.published_parsed
          elif entry.has_key('updated'):
            pdate = entry.updated_parsed
          elif entry.has_key('created'):
            pdate = entry.created_parsed
          elif entry.has_key('expired'):
            pdate = entry.expired_parsed
          # Judge latest news or old news
          pdate = datetime.datetime(*pdate[:6], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
          jst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
          if (jst_time + datetime.timedelta(days=-1)) < pdate:
            news_list.add(tuple([pdate, entry.title, entry.link]))

  webhook_url = sys.argv[1]
  main_content = {
    "username":"NEWS Bot",
  }
  main_content["embeds"] = []
  for news in news_list:
      htmldata = getdata(news[2])
      sp = BeautifulSoup(htmldata, 'html.parser')
      imgs = sp.find_all('img')
      dictimg = {}
      dictimg["url"] = imgs[0]['src']
      cn = {}
      cn["title"] = news[1]
      cn["url"] = news[2]
      cn["thumbnail"] = dictimg

      main_content["embeds"].append(cn)
  requests.post(webhook_url, json.dumps(main_content), headers={'Content-Type': 'application/json'})
  # Print all latest news
  # for news in news_list:
  #   print(news[0], news[1], news[2])

  #with open(sys.argv[1], mode='w', encoding='utf-8') as f:
  #  for news in news_list:
  #    f.write('[' + news[1] + '](' + news[2] + ')\n')


if __name__ == '__main__':
  #main()
  htmldata = getdata("https://github.com/k5-mot")
  soup = BeautifulSoup(htmldata, 'html.parser')
  imgs = soup.find_all('img')
  print(imgs[0]['src'])
