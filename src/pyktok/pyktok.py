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
                metadata_fn='', 
                comments_fn=''):
    if save_video == False and metadata_fn == '' and comments_fn == '':
        print('Since save_video, metadata_fn, and comments_fn are all False or blank, the program did nothing.')
        return

    tt_json = get_tiktok_json(video_url)
    regex_url = re.findall('(?<=@)(.+?)(?=\?|$)',video_url)[0]
    base_fn = regex_url.replace('/','_')
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
        video_fn = base_fn + '.mp4'
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
    
    if comments_fn != '':
        comments_dict = {'cid':[],
                         'video_id':[],
                         'text':[],
                         'timestamp':[],
                         'digg_count':[],
                         'status':[],
                         'reply_id':[],
                         'user_digged':[],
                         'text_extra':[],
                         'reply_comment_total':[],
                         'reply_to_reply_id':[],
                         'is_author_digged':[],
                         'stick_position':[],
                         'user_buried':[],
                         'label_list':[],
                         'author_pin':[],
                         'no_show':[],
                         'comment_lang':[],
                         'user':[]}
        comments_chunk = pd.DataFrame()
        for i in tt_json['CommentItem'].keys():
            comments_dict['cid'].append(tt_json['CommentItem'][i]['cid'])
            comments_dict['video_id'].append(tt_json['CommentItem'][i]['aweme_id'])
            comments_dict['text'].append(tt_json['CommentItem'][i]['text'])
            time = tt_json['CommentItem'][i]['create_time']
            try:
                comments_dict['timestamp'].append(datetime.fromtimestamp(int(time)).isoformat())
            except Exception:
                comments_dict['timestamp'].append('')
            try:
                comments_dict['digg_count'].append(tt_json['CommentItem'][i]['digg_count'])
            except Exception:
                comments_dict['digg_count'].append(np.nan)
            try:
                comments_dict['status'].append(tt_json['CommentItem'][i]['status'])
            except Exception:
                comments_dict['status'].append('')
            try:
                comments_dict['reply_id'].append(tt_json['CommentItem'][i]['reply_id'])
            except Exception:
                comments_dict['reply_id'].append('')
            try:
                comments_dict['user_digged'].append(tt_json['CommentItem'][i]['user_digged'])
            except Exception:
                comments_dict['user_digged'].append('')
            try:
                comments_dict['text_extra'].append(tt_json['CommentItem'][i]['text_extra'])
            except Exception:
                comments_dict['text_extra'].append('')
            try:
                comments_dict['reply_comment_total'].append(tt_json['CommentItem'][i]['reply_comment_total'])
            except Exception:
                comments_dict['reply_comment_total'].append(np.nan)
            try:
                comments_dict['reply_to_reply_id'].append(tt_json['CommentItem'][i]['reply_to_reply_id'])
            except Exception:
                comments_dict['reply_to_reply_id'].append('')
            try:
                comments_dict['is_author_digged'].append(tt_json['CommentItem'][i]['is_author_digged'])
            except Exception:
                comments_dict['is_author_digged'].append('')
            try:
                comments_dict['stick_position'].append(tt_json['CommentItem'][i]['stick_position'])
            except Exception:
                comments_dict['stick_position'].append('')
            try:
                comments_dict['user_buried'].append(tt_json['CommentItem'][i]['user_buried'])
            except Exception:
                comments_dict['user_buried'].append('')
            try:
                comments_dict['label_list'].append(tt_json['CommentItem'][i]['label_list'])
            except Exception:
                comments_dict['label_list'].append('')
            try:
                comments_dict['author_pin'].append(tt_json['CommentItem'][i]['author_pin'])
            except Exception:
                comments_dict['author_pin'].append('')
            try:
                comments_dict['no_show'].append(tt_json['CommentItem'][i]['no_show'])
            except Exception:
                comments_dict['no_show'].append('')
            try:
                comments_dict['comment_lang'].append(tt_json['CommentItem'][i]['comment_language'])
            except Exception:
                comments_dict['comment_lang'].append('')
            try:
                comments_dict['user'].append(tt_json['CommentItem'][i]['user'])
            except Exception:
                comments_dict['user'].append('')
            comments_chunk = pd.DataFrame(comments_dict)
        if os.path.exists(comments_fn):
            comments = pd.read_csv(comments_fn,keep_default_na=False)
            new_comments = pd.concat([comments,comments_chunk])
        else:
            new_comments = comments_chunk
        new_comments.to_csv(comments_fn,index=False)
        print("Saved comments for video\n",video_url,"\nto\n",os.getcwd())
        
    if save_video == True:
        tt_video_url = tt_json['ItemList']['video']['preloadList'][0]['url']
        tt_video = requests.get(tt_video_url,allow_redirects=True)
    
        with open(video_fn, 'wb') as fn:
            fn.write(tt_video.content)
        print("Saved video\n",video_url,"\nto\n",os.getcwd())

def save_tiktok_multi(video_urls,
                      save_video=True,
                      metadata_fn='',
                      comments_fn='',
                      sleep=0):
    if type(video_urls) is str:
        tt_urls = open(video_urls).read().splitlines()
    else:
        tt_urls = video_urls
    for u in tt_urls:
        save_tiktok(u,save_video,metadata_fn,comments_fn)
        time.sleep(sleep)
        