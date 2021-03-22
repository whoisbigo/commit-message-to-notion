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

# add test item
# newchild = page.children.add_new(TodoBlock, title="Something to get done")
# newchild.checked = True

commitMessage = os.environ['COMMIT_MESSAGE']
print('adding item..(commitMessage: {})'.format(commitMessage))
title = '{date} : {message}'
page.children.add_new(BulletedListBlock, title=title.format(date=get_today_str(), message=commitMessage))
print('adding item done.')
