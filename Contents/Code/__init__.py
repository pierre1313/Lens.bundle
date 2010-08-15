# Thanks to http://www.flickr.com/photos/stage88/3257281185/ for the icon.
from BeautifulSoup import BeautifulStoneSoup as BSS
import re

RSS_FEED = 'http://lens.blogs.nytimes.com/feed/'
PHOTO_NS = {'m':'http://search.yahoo.com/mrss','c':'http://purl.org/rss/1.0/modules/content/'}

####################################################################################################
def Start():
  Plugin.AddPrefixHandler("/photos/nytimeslens", PhotoMenu, 'Lens', 'icon-default.png', 'art-default.png')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'Lens'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.png')
  MediaContainer.thumb = R('icon-default.png')
  HTTP.SetCacheTime(3600*3)

####################################################################################################
def UpdateCache():
  HTTP.Request(RSS_FEED)

####################################################################################################
def PhotoMenu():
  dir = MediaContainer(viewGroup='Details', title2="Photos")
  xml = HTTP.Request(RSS_FEED).content.replace('media:content','content')
  for item in XML.ElementFromString(xml).xpath('//item'):
    title = item.find('title').text
    summary = item.xpath('description')[0].text.replace('<p>','').replace('</p>','').replace('<br />',"\n").replace(' [...]', '...')
    soup = BSS(summary, convertEntities=BSS.HTML_ENTITIES) 
    summary = soup.contents[0]
    date = Datetime.ParseDate(item.find('pubDate').text).strftime('%a %b %d, %Y')
    thumb = item.xpath('content', namespaces=PHOTO_NS)[0].get('url')
    dir.Append(Function(DirectoryItem(PhotoList, title, date, summary, thumb), key=item.find('link').text))
  return dir
  
####################################################################################################
def PhotoList(sender, key):
  dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
  data = HTTP.Request(key).content
  url = re.findall("'dataURL','([^']+.xml)'", data)[0]
  image = 1
  for photo in XML.ElementFromURL(url).xpath('//photo'):
    text = photo.find('caption').text
    url = photo.find('url').text
    dir.Append(PhotoItem(url, title='Photo %d' % image, subtitle=photo.find('credit').text, summary=text, thumb=url)) 
    image += 1
  return dir
