# -*- coding: utf-8 -*-
"""
ARM64 Compatible version of pyktok
Created on Thu Jul 14 14:06:01 2022

@author: freelon
Modified for ARM64 compatibility
"""

import asyncio
from typing import Optional
import json
import os
import random
import re
import time
from datetime import datetime

import browser_cookie3
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

global cookies
cookies = dict()

url_regex = r'(?<=\.com/)(.+?)(?=\?|$)'
video_id_regex = r'(?<=/video/)([0-9]+)'

ms_token = os.environ.get(
    "ms_token", None
)

headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}

runsb_rec = (
    'If pyktok does not operate as expected, you may find it helpful to run the \'specify_browser\' function. \'specify_browser\' takes as its sole argument a string representing a browser installed on your system, e.g. "chrome," "firefox," "edge," etc.')
runsb_err = 'No browser defined for cookie extraction. We strongly recommend you run \'specify_browser\', which takes as its sole argument a string representing a browser installed on your system, e.g. "chrome," "firefox," "edge," etc.'

print(runsb_rec)


class BrowserNotSpecifiedError(Exception):
    def __init__(self):
        super().__init__(runsb_err)


def specify_browser(browser):
    global cookies
    cookies = getattr(browser_cookie3, browser)(domain_name='.tiktok.com')


def deduplicate_metadata(metadata_fn, video_df, dedup_field='video_id'):
    if os.path.exists(metadata_fn):
        metadata = pd.read_csv(metadata_fn, keep_default_na=False)
        combined_data = pd.concat([metadata, video_df])
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
                   'author_verified',
                   'poi_name',
                   'poi_address',
                   'poi_city']
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
    try:
        data_list.append(video_obj['poi']['name'])
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_obj['poi']['address'])
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_obj['poi']['city'])
    except Exception:
        data_list.append('')
    data_row = pd.DataFrame(dict(zip(data_header, data_list)), index=[0])
    return data_row


def get_tiktok_json(video_url, browser_name=None):
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    global cookies
    if browser_name is not None:
        cookies = getattr(browser_cookie3, browser_name)(domain_name='.tiktok.com')
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    # retain any new cookies that got set in this request
    cookies = tt.cookies
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id': "SIGI_STATE"})
    try:
        tt_json = json.loads(tt_script.string)
    except AttributeError:
        return
    return tt_json


def alt_get_tiktok_json(video_url, browser_name=None):
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    global cookies
    if browser_name is not None:
        cookies = getattr(browser_cookie3, browser_name)(domain_name='.tiktok.com')
    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    # retain any new cookies that got set in this request
    cookies = tt.cookies
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id': "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
    try:
        tt_json = json.loads(tt_script.string)
    except AttributeError:
        print(
            "The function encountered a downstream error and did not deliver any data, which happens periodically for various reasons. Please try again later.")
        return None
    return tt_json


def save_tiktok(content_url,
                save_video=False,
                metadata_fn='',
                browser_name=None,
                dir_path: Optional[str] = None):
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    if save_video == False and metadata_fn == '':
        print('Since save_video and metadata_fn are both False/blank, the program did nothing.')
        return None

    tt_json = get_tiktok_json(content_url, browser_name)

    content_file_paths: list[str] = []

    if tt_json is not None:
        video_id = list(tt_json['ItemModule'].keys())[0]

        if save_video:
            regex_url = re.findall(url_regex, content_url)[0]
            if 'imagePost' in tt_json['ItemModule'][video_id]:
                slide_count = 1
                for slide in tt_json['ItemModule'][video_id]['imagePost']['images']:
                    content_file_name = regex_url.replace('/', '_') + '_slide_' + str(slide_count) + '.jpeg'
                    content_url = slide['imageURL']['urlList'][0]
                    headers['referer'] = 'https://www.tiktok.com/'
                    # include cookies with the video request
                    tt_video_response = requests.get(content_url, allow_redirects=True, headers=headers, cookies=cookies)
                    content_file_path = _save(dir_path, content_file_name, tt_video_response.content)
                    content_file_paths.append(content_file_path)
                    slide_count += 1
            else:
                regex_url = re.findall(url_regex, content_url)[0]
                content_file_name = regex_url.replace('/', '_') + '.mp4'
                try:
                    content_url = tt_json['ItemModule'][video_id]['video']['downloadAddr']
                except:
                    content_url = \
                        tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']['video'][
                            'downloadAddr']
                headers['referer'] = 'https://www.tiktok.com/'
                content_file_path = os.path.join(dir_path, content_file_name) if dir_path else content_file_name
                if os.path.exists(content_file_path):
                    print(f"File {content_file_path} already exists, skipping download")
                    content_file_paths.append(content_file_path)
                else:
                    # include cookies with the video request
                    tt_video_response = requests.get(content_url, allow_redirects=True, headers=headers, cookies=cookies)
                    content_file_path = _save(dir_path, content_file_name, tt_video_response.content)
                    content_file_paths.append(content_file_path)
                    print(f"Saved content {content_url} to {content_file_path}")

        if metadata_fn != '':
            data_slot = tt_json['ItemModule'][video_id]
            data_row = generate_data_row(data_slot)
            try:
                user_id = list(tt_json['UserModule']['users'].keys())[0]
                data_row.loc[0, "author_verified"] = tt_json['UserModule']['users'][user_id]['verified']
            except Exception:
                pass
            if os.path.exists(metadata_fn):
                metadata = pd.read_csv(metadata_fn, keep_default_na=False)
                combined_data = pd.concat([metadata, data_row])
            else:
                combined_data = data_row
            combined_data.to_csv(metadata_fn, index=False)
            return None
        return None

    else:
        tt_json = alt_get_tiktok_json(content_url, browser_name)
        video_detail = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']

        item_info = video_detail.get('itemInfo')

        if item_info is None:
            status_code = video_detail.get('statusCode')
            if status_code is not None:
                print(f"{status_code}: {video_detail.get('statusMsg')}")
                return None, None
            print(tt_json)
            raise "no itemInfo found in tt_json"

        item_struct = item_info['itemStruct']
        if save_video == True:
            regex_url = re.findall(url_regex, content_url)[0]
            content_file_name = regex_url.replace('/', '_') + '.mp4'
            try:
                content_url = item_struct['video']['playAddr']
                if content_url == '':
                    raise
            except:
                content_url = item_struct['video']['downloadAddr']
            headers['referer'] = 'https://www.tiktok.com/'
            content_file_path = os.path.join(dir_path, content_file_name) if dir_path else content_file_name

            if os.path.exists(content_file_path):
                print(f"File {content_file_path} already exists, skipping download")
                content_file_paths.append(content_file_path)
                return content_file_paths, metadata_fn

            print(f"Saving {content_url} to {content_file_path}")

            # include cookies with the video request
            with requests.get(content_url, headers=headers, stream=True, cookies=cookies,
                              timeout=60) as tt_video_response:
                tt_video_response.raise_for_status()
                with open(content_file_path, "wb") as f:
                    for chunk in tt_video_response.iter_content(chunk_size=8192):
                        if chunk:  # Skip keep-alive new chunks
                            f.write(chunk)

            content_file_paths.append(content_file_path)
            print(f"Saved content {content_url} to {content_file_path}")

        if metadata_fn != '':
            data_slot = item_struct
            data_row = generate_data_row(data_slot)
            try:
                data_row.loc[0, "author_verified"] = item_struct['author']
            except Exception:
                pass
            if os.path.exists(metadata_fn):
                metadata = pd.read_csv(metadata_fn, keep_default_na=False)
                combined_data = pd.concat([metadata, data_row])
            else:
                combined_data = data_row
            combined_data.to_csv(metadata_fn, index=False)
            print("Saved metadata for video\n", content_url, "\nto\n", os.getcwd())

        return content_file_paths, metadata_fn


def get_video_urls_selenium(tt_ent, ent_type="user", video_ct=30, headless=True):
    """
    ARM64-compatible version using Selenium instead of TikTokApi
    """
    if ent_type not in ['user', 'hashtag']:
        raise Exception('Only allowed `ent_type` values are "user" or "hashtag".')
    
    # Setup Chrome options for ARM64
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Use webdriver-manager to handle Chrome driver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url_p1 = "https://www.tiktok.com/@"
        url_p2 = "/video/"
        tt_list = []
        
        if ent_type == 'user':
            url = f"{url_p1}{tt_ent}"
        elif ent_type == 'hashtag':
            url = f"https://www.tiktok.com/tag/{tt_ent}"
        
        driver.get(url)
        time.sleep(3)
        
        # Scroll to load more videos
        for i in range(video_ct // 10 + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Find video links
        video_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')
        
        video_urls = []
        for link in video_links[:video_ct]:
            href = link.get_attribute('href')
            if href and '/video/' in href:
                video_urls.append(href)
        
        return video_urls[:video_ct]
        
    finally:
        driver.quit()


def save_tiktok_multi_urls(video_urls,
                           save_video=False,
                           metadata_fn='',
                           sleep=4,
                           browser_name=None,
                           dir_path: Optional[str] = None):
    if 'cookies' not in globals() and browser_name is None:
        raise BrowserNotSpecifiedError
    if type(video_urls) is str:
        tt_urls = open(video_urls).read().splitlines()
    else:
        tt_urls = video_urls
    for u in tt_urls:
        save_tiktok(u, save_video, metadata_fn, browser_name, dir_path=dir_path)
        time.sleep(random.randint(1, sleep))
    print('Saved', len(tt_urls), 'videos and/or lines of metadata')


def save_tiktok_multi_page(tt_ent,
                           ent_type="user",
                           video_ct=30,
                           headless=True,
                           save_video=False,
                           metadata_fn='',
                           sleep=4,
                           browser_name=None):
    video_urls = get_video_urls_selenium(tt_ent, ent_type, video_ct, headless)
    save_tiktok_multi_urls(video_urls, save_video, metadata_fn, sleep, browser_name)


def get_comments_selenium(video_url, comment_count=30, headless=True):
    """
    ARM64-compatible version for getting comments using Selenium
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(video_url)
        time.sleep(3)
        
        # Scroll to load comments
        for i in range(comment_count // 10 + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Extract comments (this is a simplified version)
        comments = []
        comment_elements = driver.find_elements(By.CSS_SELECTOR, '[data-e2e="comment-item"]')
        
        for element in comment_elements[:comment_count]:
            try:
                comment_text = element.find_element(By.CSS_SELECTOR, '[data-e2e="comment-level1"]').text
                comments.append({'text': comment_text})
            except:
                continue
        
        return pd.DataFrame(comments)
        
    finally:
        driver.quit()


def save_tiktok_comments(video_url,
                         filename='',
                         comment_count=30,
                         headless=True,
                         save_comments=True,
                         return_comments=True):
    comment_results = get_comments_selenium(video_url, comment_count, headless)
    if save_comments:
        if filename == '':
            regex_url = re.findall(url_regex, video_url)[0]
            filename = regex_url.replace('/', '_') + '_comments.csv'
        data_to_save = deduplicate_metadata(filename, comment_results, 'text')
        data_to_save.to_csv(filename, mode='w', index=False)
        print(len(comment_results), "comments saved.")
    if return_comments:
        return comment_results
    return None


def get_user_data_selenium(tt_ent, headless=True):
    """
    ARM64-compatible version for getting user data using Selenium
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = f"https://www.tiktok.com/@{tt_ent}"
        driver.get(url)
        time.sleep(3)
        
        # Extract user data from page
        user_data = {}
        try:
            # This is a simplified extraction - you may need to adjust selectors
            username = driver.find_element(By.CSS_SELECTOR, '[data-e2e="user-title"]').text
            user_data['username'] = username
        except:
            pass
        
        # Get first few videos
        video_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')
        video_data = []
        for link in video_links[:5]:
            href = link.get_attribute('href')
            if href:
                video_data.append({'url': href})
        
        return user_data, video_data
        
    finally:
        driver.quit()


def _save(dir_path: str, file_name: str, content: bytes):
    file_path = os.path.join(dir_path, file_name) if dir_path else file_name
    print(f"Saving {file_path}")

    if os.path.exists(file_path):
        print(f"File {file_path} already exists. Skipping save.")
        return file_path

    with open(file_path, 'wb') as fn:
        fn.write(content)
    return file_path
