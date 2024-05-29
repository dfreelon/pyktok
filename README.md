## Pyktok
**A simple module to collect video, text, and metadata from TikTok.**

We developed Pyktok ("pick-tock") because none of the existing TikTok data collection utilities we could find suited our needs. Pyktok pulls its data directly from the JSON objects embedded in Tiktok pages and from hidden APIs with no public documentation. Here are its major features:

 - Download TikTok videos
 - Download video metadata
 - Download 15-30 videos and/or metadata lines from hashtag, user, and music pages displaying multiple videos
 - Download full TikTok JSON data objects (in case you want to extract data from parts of the object not included in the above functions)

R users, check out [traktok](https://github.com/JBGruber/traktok), an R port of Pyktok.

This program may stop working suddenly if TikTok changes how it stores its data (see [Freelon, 2018](https://osf.io/preprints/socarxiv/56f4q/)). Some functions may require you to be logged in to TikTok, which means they may not work on cloud servers that don't have Chrome or Firefox installed.

TikTok now offers an official research API to US-based academics--[you can apply for access here](https://developers.tiktok.com/products/research-api/).

Please note that [a number of US states have banned TikTok on state-owned devices](https://www.reuters.com/world/us/wisconsin-governor-signs-order-banning-tiktok-state-devices-2023-01-12/), which may include IT resources provided by state universities. Individuals employed by such institutions are advised to use Pyktok only within applicable laws and regulations.

**Installation**

```pip install pyktok```

**Requirements**

Pyktok relies on the following packages:

 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - [browser-cookie3](https://pypi.org/project/browser-cookie3/)
 - [Numpy](https://numpy.org/)
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)
 - [Selenium](https://pypi.org/project/selenium/)
 - [Streamlit](https://streamlit.io/)

**Usage**

```python
import pyktok as pyk
pyk.specify_browser('chrome') 
```
We strongly recommend you run the `specify_browser` function first to initialize Pyktok with a cookie from your browser of choice (e.g. 'firefox,' 'edge' etc.). If you don't, you must use the `browser_name` parameter in most other functions, otherwise they will throw an error.

Please note that functions that start with "get" will return data to working memory, while those starting with "save" will save data to disk without returning anything.

To download a single TikTok video and one line of metadata to the file "video_data.csv" (`'chrome'` can be changed to `'firefox'` if necessary):
```python    
pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7106594312292453675?is_copy_url=1&is_from_webapp=v1',
	        True,
                'video_data.csv',
		'chrome')
```    
To download another TikTok video and add its metadata to the same file as above:
```python   
pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1',
	        True,
                'video_data.csv',
		'chrome')
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
To download up to 30 metadata lines from a *user* page (note, for this to work you must set the `browser_name` parameter to a browser on your system that you have used to access TikTok *and* that is supported by `browser_cookie3`. I think the only valid values are `'chrome'` and `'firefox'`. Also you can get the videos by setting `save_video` to `True`): 

```python    
pyk.save_tiktok_multi_page('https://www.tiktok.com/@tiktok',save_video=False,save_metadata=True,browser_name='chrome')
```

To download up to 15 metadata lines from a *hashtag* page: 

```python    
pyk.save_tiktok_multi_page('https://www.tiktok.com/tag/datascience?lang=en',save_video=False,save_metadata=True)
```

To download up to 15 metadata lines from a *music* page: 

```python    
pyk.save_tiktok_multi_page('https://www.tiktok.com/music/Anti-Hero-7156822419213125634?lang=en',save_video=False,save_metadata=True)
```
                       
To get an individual video's JSON object:
```python	
tt_json = pyk.get_tiktok_json('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1')
```

TikTok's servers may not love it if you run some of the above functions at full speed, so I recommend increasing the `sleep` parameter if you get autobanned. I haven't tested this extensively so I have no idea if or when autobans start to kick in.

Pyktok can also be run from a browser window using `streamlit`. To do so, simply navigate to your `pyktok` directory in a command prompt (it should contain the file `app.py`) and run `streamlit run app.py`. This should pop up a browser window that allows you to control Pyktok using graphical affordances.

Mostly by [@dfreelon](https://github.com/dfreelon/) with contributions from (in chronological order): 
- [@pkreissel](https://github.com/pkreissel)
- [@p-bach](https://github.com/p-bach)
- [@TimoBaeuerle](https://github.com/TimoBaeuerle)
- [@christinapwalker](https://github.com/christinapwalker)
- [@codeteme](https://github.com/codeteme)
- [@dphiffer](https://github.com/dphiffer)
- [@BillyBSig](https://github.com/BillyBSig)


### Testing
From the root folder, run in the terminal:
```shell
pip install pytest
pytest
```