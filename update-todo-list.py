from notion.client import NotionClient
from notion.block import *
from notion.collection import *
from datetime import datetime
import notion
import os

def get_today_str():
  today = datetime.today()
  return f'{today.year}-{today.month}-{today.day}' 

print('creating client..')
tokenV2 = os.environ['NOTION_TOKEN_V2']
client = NotionClient(token_v2=tokenV2)
print('creating client done.')

pageUrl = os.environ['NOTION_PAGE_URL']
print('getting page..(pageUrl: {})'.format(pageUrl))
page = client.get_block(pageUrl, force_refresh=True)
print('getting page done.(title:{})'.format(page.title))
# page.title = '{} - edited by github action'.format(page.title)



# find today's title
titleToday = get_today_str()
today = None
for child in page.children:
  if child.title == titleToday:
    today = child
    break

if today == None:
  today = page.children.add_new(ToggleBlock, title=titleToday)

today.move_to(page, "first-child")

commitMessage = os.environ['COMMIT_MESSAGE']
messageList = commitMessage.split(', ')

for message in messageList:
  print('adding item..(commitMessage: {})'.format(commitMessage))
  #title = '{date} : {message}'
  title = '{message}'
  newchild = today.children.add_new(TodoBlock, title=title.format(message=commitMessage))
  newchild.checked = True
  print('adding item done.')
