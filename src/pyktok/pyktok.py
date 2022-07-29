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

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

def get_account_video_urls(user_url):
    tt_json = get_tiktok_json(user_url)
    video_ids = tt_json['ItemList']['user-post']['list']
    tt_account = tt_json['UserPage']['uniqueId']
    url_seg_1 = 'https://www.tiktok.com/@'
    url_seg_2 = '/video/'
    video_urls = [url_seg_1 + tt_account + url_seg_2 + u for u in video_ids]
    return video_urls

def get_tiktok_json(video_url):
    cookies = browser_cookie3.chrome(domain_name='.tiktok.com')
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id':"SIGI_STATE"})
    tt_json = json.loads(tt_script.string)
    return tt_json

def save_tiktok(video_url,
                save_video=True,
                metadata_fn=''):
    if save_video == False and metadata_fn == '':
        print('Since save_video and metadata_fn are both False/blank, the program did nothing.')
        return

    tt_json = get_tiktok_json(video_url)
    regex_url = re.findall('(?<=@)(.+?)(?=\?|$)',video_url)[0]
    video_fn = regex_url.replace('/','_') + '.mp4'
    video_id = list(tt_json['ItemModule'].keys())[0]
    
    if metadata_fn != '':
        data_header = ['video_id',
                       'video_timestamp',
                       'video_length',
                       'video_title',
                       'video_locationcreated',
                       'video_diggcount',
                       'video_sharecount',
                       'video_commentcount',
                       'video_playcount',
                       'video_description',                       
                       'video_is_ad',
                       'video_fn',
                       'author_username',
                       'author_name',
                       'author_followercount',
                       'author_followingcount',
                       'author_heartcount',
                       'author_videocount',
                       'author_diggcount']
        time = tt_json['ItemModule'][video_id]['createTime']
        try:
            video_timestamp = datetime.fromtimestamp(int(time)).isoformat()
        except Exception:
            video_timestamp = ''
        try:
            video_length = tt_json['ItemModule'][video_id]['video']['duration']
        except Exception:
            video_length = np.nan
        try:
            video_title = tt_json['ItemModule'][video_id]['desc']
        except Exception:
            video_title = ''
        try:
            video_locationcreated = tt_json['ItemModule'][video_id]['locationCreated']
        except Exception:
            video_locationcreated = ''
        try:
            video_diggcount = tt_json['ItemModule'][video_id]['stats']['diggCount']
        except Exception:
            video_diggcount = np.nan
        try:
            video_sharecount = tt_json['ItemModule'][video_id]['stats']['shareCount']
        except Exception:
            video_sharecount = np.nan
        try:
            video_commentcount = tt_json['ItemModule'][video_id]['stats']['commentCount']
        except Exception:
            video_commentcount = np.nan
        try:
            video_playcount = tt_json['ItemModule'][video_id]['stats']['playCount']
        except Exception:
            video_playcount = np.nan
        try:
            video_description = tt_json['ItemModule'][video_id]['desc']
        except Exception:
            video_description = ''
        try:
            video_is_ad = tt_json['ItemModule'][video_id]['isAd']
        except Exception:
            video_is_ad = ''
        try:
            author_username = tt_json['ItemModule'][video_id]['author']
        except Exception:
            author_username = ''
        try:
            author_name = tt_json['ItemModule'][video_id]['authorName']
        except Exception:
            try:
                author_name = tt_json['ItemModule'][video_id]['nickname']
            except Exception:
                author_name = ''
        try:
            author_followercount = tt_json['ItemModule'][video_id]['authorStats']['followerCount']
        except Exception:
            author_followercount = np.nan
        try:
            author_followingcount = tt_json['ItemModule'][video_id]['authorStats']['followingCount']
        except Exception:
            author_followingcount = np.nan   
        try:
            author_heartcount = tt_json['ItemModule'][video_id]['authorStats']['heartCount']
        except Exception:
            author_heartcount = np.nan    
        try:
            author_videocount = tt_json['ItemModule'][video_id]['authorStats']['videoCount']
        except Exception:
            author_videocount = np.nan    
        try:
            author_diggcount = tt_json['ItemModule'][video_id]['authorStats']['diggCount']
        except Exception:
            author_diggcount = np.nan
        data_list = [video_id,
                     video_timestamp,
                     video_length,
                     video_title,
                     video_locationcreated,
                     video_diggcount,
                     video_sharecount,
                     video_commentcount,
                     video_playcount,
                     video_description,
                     video_is_ad,
                     video_fn,
                     author_username,
                     author_name,
                     author_followercount,
                     author_followingcount,
                     author_heartcount,
                     author_videocount,
                     author_diggcount]
        data_line = pd.DataFrame(dict(zip(data_header,data_list)),index=[0])
        if os.path.exists(metadata_fn):
            metadata = pd.read_csv(metadata_fn,keep_default_na=False)
            new_data = pd.concat([metadata,data_line])
        else:
            new_data = data_line
        new_data.to_csv(metadata_fn,index=False)
        print("Saved metadata for video\n",video_url,"\nto\n",os.getcwd())
        
    if save_video == True:
        tt_video_url = tt_json['ItemList']['video']['preloadList'][0]['url']
        tt_video = requests.get(tt_video_url,allow_redirects=True)
    
        with open(video_fn, 'wb') as fn:
            fn.write(tt_video.content)
        print("Saved video\n",video_url,"\nto\n",os.getcwd())

def save_tiktok_multi(video_urls,
                      save_video=True,
                      metadata_fn='',
                      sleep=0):
    if type(video_urls) is str:
        tt_urls = open(video_urls).read().splitlines()
    else:
        tt_urls = video_urls
    for u in tt_urls:
        save_tiktok(u,save_video,metadata_fn)
        time.sleep(random.randint(1, sleep))

def save_video_comments(video_url,
                        comments_file,
                        max_comments=np.inf,
                        sleep=4):
    cursor = 0
    headers["referer"] = video_url
    video_id = re.findall('(?<=/video/)(.+?)(?=\?|$)',video_url)[0]
    while cursor < max_comments:
        params = {'aweme_id': video_id,
                  'count': '20',
                  'cursor': str(cursor)
                 }
        cookies = browser_cookie3.chrome(domain_name='.tiktok.com')
        try:
            response = requests.get('https://www.tiktok.com/api/comment/list/',
                                    headers=headers,
                                    params=params,
                                    cookies=cookies
                                    )
            data = response.json()
            cursor = cursor + len(data['comments'])
            print(cursor,"comments downloaded (max "+ str(max_comments) +")")
            if os.path.exists(comments_file):
                pd.DataFrame(data['comments']).to_csv(comments_file,
                                                      mode='a',
                                                      header=False,
                                                      index=False)
            else:
                pd.DataFrame(data['comments']).to_csv(comments_file,index=False)
            if data["has_more"] != 1:
                break
            time.sleep(random.randint(1, sleep))
        except Exception as e:
            print(e)
