## Pyktok
<!---
/* $\color{red} NOTE:\ 2025-01-19:\ A\ nationwide\ TikTok\ ban\ is\ now\ in\ effect\ in\ the\ US.\$ */

$\color{red}All\ Pyktok\ updates\ are\ suspended\ until\ the\ ban\ is\ lifted.\$
-->
**A simple module to collect video, text, and metadata from TikTok.**

We developed Pyktok ("pick-tock") because none of the existing TikTok data collection utilities we could find suited our needs. Pyktok pulls its data directly from the JSON objects embedded in Tiktok pages and from hidden APIs with no public documentation. Here are its major features:

 - Download TikTok videos
 - Download video metadata
 - Download around 30 videos and/or metadata lines from hashtag, user, and the "You May Like" sections of video pages (you can try to specify the exact number but TikTok doesn't always follow it exactly)
 - Download video comments
 - Download full TikTok JSON data objects (in case you want to extract data from parts of the object not included in the above functions)

**Like Pyktok? Want to say thanks (and help fund future updates)? I accept [Venmo](https://venmo.com/Deen-Freelon) and [Cash App](https://cash.app/$dfreelon).**

R users, check out [traktok](https://github.com/JBGruber/traktok), an R port of Pyktok.

This program may stop working suddenly if TikTok changes how it stores its data (see [Freelon, 2018](https://osf.io/preprints/socarxiv/56f4q/)). Some functions may require you to be logged in to TikTok, which means they may not work on cloud servers that don't have Chrome or Firefox installed.

TikTok now offers an official research API to US-based academics--[you can apply for access here](https://developers.tiktok.com/products/research-api/).

Please note that [a number of US states have banned TikTok on state-owned devices](https://www.reuters.com/world/us/wisconsin-governor-signs-order-banning-tiktok-state-devices-2023-01-12/), which may include IT resources provided by state universities. Individuals employed by such institutions are advised to use Pyktok only within applicable laws and regulations.

**Installation**

1. ```pip install pyktok```
2. You'll also need to install the binaries for playwright using the `playwright install` (and possibly `playwright install-deps`) command in your local console.

**Requirements**

Pyktok relies on the following external packages:

 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - [browser-cookie3](https://pypi.org/project/browser-cookie3/)
 - [Numpy](https://numpy.org/)
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)
 - [Streamlit](https://streamlit.io/)
 - [TikTokApi](https://github.com/davidteather/TikTok-Api)

**Usage**

```python
import pyktok as pyk
pyk.specify_browser('chrome') #browser specification may or may not be necessary depending on your local settings
```
Historically it has been prudent to run the `specify_browser` function first to initialize Pyktok with a cookie from your browser of choice (e.g. 'firefox,' 'edge' etc.). However, recent developments indicate this may not be necessary for all users. YMMV.

Please note that functions that start with "get" will return data to working memory, while those starting with "save" will save data to disk without returning anything.

To download a single TikTok video and one line of metadata to the file "video_data.csv":
```python    
pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7106594312292453675?is_copy_url=1&is_from_webapp=v1',
	        True,
                'video_data.csv')
```    
To download another TikTok video and add its metadata to the same file as above:
```python   
pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1',
	        True,
                'video_data.csv')
```   
To download metadata ONLY from the video URLs used in the preceding two lines of code (to also download the videos, change ```False``` to ```True```). If TikTok autobans the scraper, try changing the 1 to a higher number to increase the number of seconds between executions.
```python
tiktok_videos = ['https://www.tiktok.com/@tiktok/video/7106594312292453675?is_copy_url=1&is_from_webapp=v1',
                 'https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1']
pyk.save_tiktok_multi_urls(tiktok_videos,
                           False,
                     	  'tiktok_data.csv',
                     	   1)
```

To download around 30 metadata lines from a *user* page (you can get the videos by setting `save_video` to `True`): 

```python    
pyk.save_tiktok_multi_page('tiktok',ent_type='user',save_video=False,metadata_fn='tiktok.csv')
```

If this or the following two functions delivers an `EmptyResponseException`, try setting `headless=False`.

To download around 30 metadata lines from a *hashtag* page: 

```python    
pyk.save_tiktok_multi_page('datascience',ent_type='hashtag',save_video=False,metadata_fn='datascience.csv')
```

To download around 30 metadata lines from related videos from a *video* page: 

```python    
pyk.save_tiktok_multi_page('https://www.tiktok.com/@tiktok/video/7106594312292453675',ent_type='video_related',save_video=False,metadata_fn='7106594312292453675.csv')
```

To download around 30 comments from a video (the underlying code interprets `comment_count` rather loosely): 

```python    
pyk.save_tiktok_comments('https://www.tiktok.com/@tiktok/video/7106594312292453675',comment_count=30,save_comments=True,return_comments=False)
```
                       
To get an individual video's JSON object:
```python	
tt_json = pyk.alt_get_tiktok_json('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1')
```

TikTok's servers may not love it if you run some of the above functions at full speed, so I recommend increasing the `sleep` parameter if you get autobanned. I haven't tested this extensively so I have no idea if or when autobans start to kick in.

Pyktok can also be run from a browser window using `streamlit`. To do so, simply navigate to your `pyktok` directory in a command prompt (it should contain the file `app.py`) and run `streamlit run app.py`. This should pop up a browser window that allows you to control Pyktok using graphical affordances.

Mostly written by [@dfreelon](https://github.com/dfreelon/) with contributions from (in chronological order): 
- [@pkreissel](https://github.com/pkreissel)
- [@p-bach](https://github.com/p-bach)
- [@TimoBaeuerle](https://github.com/TimoBaeuerle)
- [@christinapwalker](https://github.com/christinapwalker)
- [@codeteme](https://github.com/codeteme)
- [@dphiffer](https://github.com/dphiffer)
- [@BillyBSig](https://github.com/BillyBSig)
- [@tomasruizt](https://github.com/tomasruizt)
