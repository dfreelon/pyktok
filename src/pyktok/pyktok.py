# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 14:06:01 2022

@author: freelon
"""

import browser_cookie3
from bs4 import BeautifulSoup
from datetime import datetime
import json
import numpy as np
import os
import pandas as pd
import random
import re
import requests
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeiumService #sic
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager

headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}
cookies = browser_cookie3.load()
url_regex = '(?<=\.com/)(.+?)(?=\?|$)'

def deduplicate_metadata(metadata_fn,video_df,dedup_field='video_id'):
    if os.path.exists(metadata_fn):
        metadata = pd.read_csv(metadata_fn,keep_default_na=False)
        combined_data = pd.concat([metadata,video_df])
        combined_data[dedup_field] = combined_data[dedup_field].astype(str)
    else:
        combined_data = video_df
    return combined_data.drop_duplicates(dedup_field)

def generate_data_row(video_obj):
    data_header = ['video_id',
                   'video_timestamp',
                   'video_duration',
                   'video_locationcreated',
                   'video_diggcount',
                   'video_sharecount',
                   'video_commentcount',
                   'video_playcount',
                   'video_description',
                   'video_is_ad',
                   'video_stickers',
                   'author_username',
                   'author_name',
                   'author_followercount',
                   'author_followingcount',
                   'author_heartcount',
                   'author_videocount',
                   'author_diggcount',
                   'author_verified']
    data_list = []
    data_list.append(video_obj['id'])
    try:
        ctime = video_obj['createTime']
        data_list.append(datetime.fromtimestamp(int(ctime)).isoformat())
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_obj['video']['duration'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['locationCreated'])
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_obj['stats']['diggCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['stats']['shareCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['stats']['commentCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['stats']['playCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['desc'])
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_obj['isAd'])
    except Exception:
        data_list.append(False)
    try:
        video_stickers = []
        for sticker in video_obj['stickersOnItem']:
            for text in sticker['stickerText']:
                video_stickers.append(text)
        data_list.append(';'.join(video_stickers))
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_obj['author']['uniqueId'])
    except Exception:
        try:
            data_list.append(video_obj['author'])
        except Exception:
            data_list.append('')
    try:
        data_list.append(video_obj['author']['nickname'])
    except Exception:
        try:
            data_list.append(video_obj['nickname'])
        except Exception:
            data_list.append('')
    try:
        data_list.append(video_obj['authorStats']['followerCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['authorStats']['followingCount'])
    except Exception:
        data_list.append(np.nan)   
    try:
        data_list.append(video_obj['authorStats']['heartCount'])
    except Exception:
        data_list.append(np.nan)   
    try:
        data_list.append(video_obj['authorStats']['videoCount'])
    except Exception:
        data_list.append(np.nan)    
    try:
        data_list.append(video_obj['authorStats']['diggCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_obj['author']['verified'])
    except Exception:
        data_list.append(False)
    data_row = pd.DataFrame(dict(zip(data_header,data_list)),index=[0])
    return data_row
#currently unused, but leaving it in case it's needed later
'''
def fix_tt_url(tt_url):
    if 'www.' not in tt_url.lower():
        url_parts = tt_url.split('://')
        fixed_url = url_parts[0] + '://www.' + url_parts[1]
        return fixed_url
    else:
        return tt_url
'''
def get_tiktok_json(video_url,browser_name=None):
    global cookies
    if browser_name is not None:
        cookies = getattr(browser_cookie3,browser_name)(domain_name='www.tiktok.com')
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id':"SIGI_STATE"})
    try:
        tt_json = json.loads(tt_script.string)
    except AttributeError:
        print("The function encountered a downstream error and did not deliver any data, which happens periodically for various reasons. Please try again later.")
        return
    return tt_json

def save_tiktok(video_url,
                save_video=True,
                metadata_fn='',
                browser_name=None):
    if save_video == False and metadata_fn == '':
        print('Since save_video and metadata_fn are both False/blank, the program did nothing.')
        return

    tt_json = get_tiktok_json(video_url,browser_name)
    video_id = list(tt_json['ItemModule'].keys())[0]

    if save_video == True:
        regex_url = re.findall(url_regex,video_url)[0]
        video_fn = regex_url.replace('/','_') + '.mp4'
        tt_video_url = tt_json['ItemModule'][video_id]['video']['downloadAddr']
        headers['referer'] = 'https://www.tiktok.com/'
        tt_video = requests.get(tt_video_url,allow_redirects=True,headers=headers)
        with open(video_fn, 'wb') as fn:
            fn.write(tt_video.content)
        print("Saved video\n",tt_video_url,"\nto\n",os.getcwd())
    
    if metadata_fn != '':
        data_slot = tt_json['ItemModule'][video_id]
        data_row = generate_data_row(data_slot)
        try:
            user_id = list(tt_json['UserModule']['users'].keys())[0]
            data_row.loc[0,"author_verified"] = tt_json['UserModule']['users'][user_id]['verified']
        except Exception:
            pass
        if os.path.exists(metadata_fn):
            metadata = pd.read_csv(metadata_fn,keep_default_na=False)
            combined_data = pd.concat([metadata,data_row])
        else:
            combined_data = data_row
        combined_data.to_csv(metadata_fn,index=False)
        print("Saved metadata for video\n",video_url,"\nto\n",os.getcwd())
        
def save_tiktok_multi_page(tiktok_url, #can be a user, hashtag, or music URL
                           save_video=False,
                           save_metadata=True,
                           metadata_fn='',
                           browser_name=None):
    tt_json = get_tiktok_json(tiktok_url,browser_name)
    data_loc = tt_json['ItemModule']
    regex_url = re.findall(url_regex,tiktok_url)[0]
    video_fn = 'tiktok_com_' + regex_url.replace('/','_') + '.mp4'
    if save_metadata == True and metadata_fn == '':
        metadata_fn = regex_url.replace('/','_') + '.csv'
    data = pd.DataFrame()
    
    for v in data_loc:
        data = pd.concat([data,generate_data_row(data_loc[v])])
        if save_video == True:
            video_url = 'https://www.tiktok.com/@' + data_loc[v]['author'] + '/video/' + data_loc[v]['id']
            save_tiktok(video_url,True)
    if save_metadata == True:
        data = deduplicate_metadata(metadata_fn,data)
        data.to_csv(metadata_fn,index=False)
    print('Saved',len(data_loc),'videos and/or lines of metadata')

def save_tiktok_multi_urls(video_urls,
                           save_video=True,
                           metadata_fn='',
                           sleep=4,
                           browser_name=None):
    if type(video_urls) is str:
        tt_urls = open(video_urls).read().splitlines()
    else:
        tt_urls = video_urls
    for u in tt_urls:
        save_tiktok(u,save_video,metadata_fn,browser_name)
        time.sleep(random.randint(1, sleep))
    print('Saved',len(tt_urls),'videos and/or lines of metadata')
    
def save_visible_comments(video_url,
                          comment_fn=None,
                          browser='chromium'):
    start_time = time.time()
    c_options = ChromeOptions()
    c_options.add_argument("--headless")
    f_options = FirefoxOptions()
    f_options.add_argument("--headless")
    if browser == 'chromium':
        driver = webdriver.Chrome(service=ChromeiumService(
                                          ChromeDriverManager(
                                          chrome_type=ChromeType.CHROMIUM).install()),
                                  options=c_options)
    elif browser == 'chrome':
        driver = webdriver.Chrome(service=ChromeiumService(
                                          ChromeDriverManager().install()),
                                  options=c_options)
    elif browser == 'firefox':
        driver = webdriver.Firefox(service=FirefoxService(
                                           GeckoDriverManager().install()),
                                   options=f_options)
    driver.get(video_url)
    try:
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'SpanUserNameText')]")))
    except TimeoutException:
        print(video_url,"has no comments")
        return
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ids_tags = soup.find_all('div',{'class':re.compile('DivCommentContentContainer')})
    comment_ids = [i.get('id') for i in ids_tags]
    names_tags = soup.find_all('a',attrs={'class':re.compile("StyledUserLinkName")})
    styled_names = [i.text.strip() for i in names_tags]
    screen_names = [i.get('href').replace('/','') for i in names_tags]
    comments_tags = soup.find_all('p',attrs={'class':re.compile("PCommentText")})
    comments = [i.text.strip() for i in comments_tags]
    likes_tags = soup.find_all('span',attrs={'class':re.compile('SpanCount')})
    likes = [int(i.text.strip()) 
             if i.text.strip().isnumeric() 
             else i.text.strip() 
             for i 
             in likes_tags]
    timestamp = datetime.now().isoformat()
    data_header = ['comment_id','styled_name','screen_name','comment','like_count','video_url','time_collected']
    data_list = [comment_ids,styled_names,screen_names,comments,likes,[video_url]*len(likes),[timestamp]*len(likes)]
    data_frame = pd.DataFrame(data_list,index=data_header).T
    
    if comment_fn is None:
        regex_url = re.findall(url_regex,video_url)[0]
        comment_fn = regex_url.replace('/','_') + '_tiktok_comments.csv'
    combined_data = deduplicate_metadata(comment_fn,data_frame,'comment_id')
    combined_data.to_csv(comment_fn,index=False)
    print('Comments saved to file',comment_fn,'in',round(time.time() - start_time,2),'secs.')
    