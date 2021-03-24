from notion.client import NotionClient
from notion.block import *
from notion.collection import *
from datetime import datetime
import notion
import os
import json

def get_commit_messages():
  messageList = []
  with open(os.environ['GITHUB_EVENT_PATH']) as json_file:
    webhookEventPayload = json.load(json_file)
    for commitItem in webhookEventPayload['commits']:
      messageList = messageList + commitItem['message'].split(', ')

  return messageList

def get_today_str():
  today = datetime.today()
  return f'{today.year}-{today.month}-{today.day}' 

print('creating client..')
tokenV2 = os.environ['NOTION_TOKEN_V2']
client = NotionClient(token_v2=tokenV2)
print('creating client done.')

pageUrl = os.environ['NOTION_PAGE_URL']
pageUrlEnvName = os.environ['NOTION_PAGE_URL_ENV_NAME']
if not(pageUrlEnvName is None):
  pageUrl = os.environ[pageUrlEnvName]

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

if today is None:
  today = page.children.add_new(ToggleBlock, title=titleToday)

today.move_to(page, 'first-child')

#commitMessage = os.environ['COMMIT_MESSAGE']
messageList = get_commit_messages()

for message in messageList:
  print('adding item..(message: {})'.format(message))
  #title = '{date} : {message}'
  title = '{message}'
  newchild = today.children.add_new(TodoBlock, title=title.format(message=message))
  newchild.checked = True
  print('adding item done.')
