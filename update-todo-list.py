from notion.client import NotionClient
from notion.block import *
from notion.collection import *
from datetime import datetime
import notion
import os

print('creating client..')
tokenV2 = os.environ['NOTION_TOKEN_V2']
client = NotionClient(token_v2=tokenV2)
print('creating client done.')

pageUrl = os.environ['NOTION_PAGE_URL']
print('getting page..(pageUrl: {})'.format(pageUrl))
page = client.get_block(pageUrl, force_refresh=True)
print('getting page done.(title:{})'.format(page.title))
# page.title = '{} - edited by github action'.format(page.title)

commitMessage = os.environ['COMMIT_MESSAGE']
print('adding item..(commitMessage: {})'.format(commitMessage))
#title = '{date} : {message}'
title = '{message}'
newchild = page.children.add_new(TodoBlock, title=title.format(message=commitMessage))
newchild.checked = True
print('adding item done.')
