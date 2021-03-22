from notion.client import NotionClient
from notion.block import *
from notion.collection import *
from datetime import datetime
import notion
import os

def get_today_str():
  today = datetime.today()
  return f'{today.year}년 {today.month}월 {today.day}일' 

print('creating client..')
tokenV2 = os.environ['NOTION_TOKEN_V2']
client = NotionClient(token_v2=tokenV2)
print('creating client done.')

print('getting page..')
pageUrl = os.environ['NOTION_PAGE_URL']
page = client.get_block(pageUrl, force_refresh=True)
print('getting page done.')

print('adding item..')
commitMessage = os.environ['COMMIT_MESSAGE']
title = '{date} : {message}'
page.children.add_new(BulletedListBlock, title=title.format(date=get_today_str, message=commitMessage))
print('adding item done.')
