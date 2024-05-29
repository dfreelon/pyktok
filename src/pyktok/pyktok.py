# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 14:06:01 2022

@author: freelon
"""
from __future__ import annotations  # make type hints work with older Python versions
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


headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}
url_regex = '(?<=\.com/)(.+?)(?=\?|$)'
runsb_rec = 'We strongly recommend you run \'specify_browser\' first, which will allow you to run pyktok\'s functions without using the browser_name parameter every time. \'specify_browser\' takes as its sole argument a string representing a browser installed on your system, e.g. "chrome," "firefox," "edge," etc.'
runsb_err = 'No browser defined for cookie extraction. We strongly recommend you run \'specify_browser\', which takes as its sole argument a string representing a browser installed on your system, e.g. "chrome," "firefox," "edge," etc.'

print(runsb_rec)

class BrowserNotSpecifiedError(Exception):
    def __init__(self):
        super().__init__(runsb_err)

def specify_browser(browser: str | None):
    global cookies
    if browser is None:
        cookies = dict()
    else:
        cookies = getattr(browser_cookie3,browser)(domain_name='www.tiktok.com')
    
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
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    global cookies
    if browser_name is not None:
        cookies = getattr(browser_cookie3,browser_name)(domain_name='www.tiktok.com')
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    # retain any new cookies that got set in this request
    cookies = tt.cookies
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id':"SIGI_STATE"})
    try:
        tt_json = json.loads(tt_script.string)
    except AttributeError:
        return
    return tt_json


def alt_get_tiktok_json(video_url,browser_name=None):
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    global cookies
    if browser_name is not None:
        cookies = getattr(browser_cookie3,browser_name)(domain_name='www.tiktok.com')
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    # retain any new cookies that got set in this request
    cookies = tt.cookies
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id':"__UNIVERSAL_DATA_FOR_REHYDRATION__"})
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
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    if save_video == False and metadata_fn == '':
        print('Since save_video and metadata_fn are both False/blank, the program did nothing.')
        return

    tt_json = get_tiktok_json(video_url,browser_name)

    if tt_json is not None:
        video_id = list(tt_json['ItemModule'].keys())[0]

        if save_video == True:
            regex_url = re.findall(url_regex, video_url)[0]
            if 'imagePost' in tt_json['ItemModule'][video_id]:
                slidecount = 1
                for slide in tt_json['ItemModule'][video_id]['imagePost']['images']:
                    video_fn = regex_url.replace('/', '_') + '_slide_' + str(slidecount) + '.jpeg'
                    tt_video_url = slide['imageURL']['urlList'][0]
                    headers['referer'] = 'https://www.tiktok.com/'
                    # include cookies with the video request
                    tt_video = requests.get(tt_video_url, allow_redirects=True, headers=headers, cookies=cookies)
                    with open(video_fn, 'wb') as fn:
                        fn.write(tt_video.content)
                    slidecount += 1
            else:
                regex_url = re.findall(url_regex, video_url)[0]
                video_fn = regex_url.replace('/', '_') + '.mp4'
                tt_video_url = tt_json['ItemModule'][video_id]['video']['downloadAddr']
                headers['referer'] = 'https://www.tiktok.com/'
                # include cookies with the video request
                tt_video = requests.get(tt_video_url, allow_redirects=True, headers=headers, cookies=cookies)
            with open(video_fn, 'wb') as fn:
                fn.write(tt_video.content)
            print("Saved video\n", tt_video_url, "\nto\n", os.getcwd())

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

    else:
        tt_json = alt_get_tiktok_json(video_url,browser_name)
        regex_url = re.findall(url_regex, video_url)[0]
        video_fn = regex_url.replace('/', '_') + '.mp4'
        tt_video_url = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']['video']['downloadAddr']
        headers['referer'] = 'https://www.tiktok.com/'
        # include cookies with the video request
        tt_video = requests.get(tt_video_url, allow_redirects=True, headers=headers, cookies=cookies)
        with open(video_fn, 'wb') as fn:
            fn.write(tt_video.content)

        if metadata_fn != '':
            data_slot = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']
            data_row = generate_data_row(data_slot)
            try:
                user_id = list(tt_json['UserModule']['users'].keys())[0]
                data_row.loc[0,"author_verified"] = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']['author']
            except Exception:
                pass
            if os.path.exists(metadata_fn):
                metadata = pd.read_csv(metadata_fn,keep_default_na=False)
                combined_data = pd.concat([metadata,data_row])
            else:
                combined_data = data_row
            combined_data.to_csv(metadata_fn,index=False)

    if save_video == True:
        print("Saved video\n", tt_video_url, "\nto\n", os.getcwd())
    if metadata_fn != '':
        print("Saved metadata for video\n",video_url,"\nto\n",os.getcwd())

def save_tiktok_multi_page(tiktok_url, #can be a user, hashtag, or music URL
                           save_video=False,
                           save_metadata=True,
                           metadata_fn='',
                           browser_name=None):
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    tt_json = get_tiktok_json(tiktok_url,browser_name)
    data_loc = tt_json['ItemModule']
    regex_url = re.findall(url_regex,tiktok_url)[0]
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
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    if type(video_urls) is str:
        tt_urls = open(video_urls).read().splitlines()
    else:
        tt_urls = video_urls
    for u in tt_urls:
        save_tiktok(u,save_video,metadata_fn,browser_name)
        time.sleep(random.randint(1, sleep))
    print('Saved',len(tt_urls),'videos and/or lines of metadata')
