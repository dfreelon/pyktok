## Pyktok
**A simple module to collect video, text, and metadata from TikTok.**

By @dfreelon with contributions from [@pkreissel](https://github.com/pkreissel), [@p-bach](https://github.com/p-bach), and [@TimoBaeuerle](https://github.com/TimoBaeuerle) 

We developed Pyktok ("pick-tock") because none of the existing TikTok data collection utilities we could find suited our needs. Pyktok pulls its data directly from the JSON objects embedded in Tiktok pages and from hidden APIs with no public documentation. Here are its major features, most of which require the URL(s) of the content you wish to collect:

 - Download TikTok videos
 - Download video metadata
 - Download up to 20 video comments
 - Download 15-30 videos and/or metadata lines from hashtag, user, and music pages displaying multiple videos
 - Download full TikTok JSON data objects (in case you want to extract data from parts of the object not included in the above functions)
 - Download TikTok metadata and video from search pages (thanks [@p-bach](https://github.com/p-bach) and [@TimoBaeuerle](https://github.com/TimoBaeuerle))
 
This program may stop working suddenly if TikTok changes how it stores its data (see [Freelon, 2018](https://osf.io/preprints/socarxiv/56f4q/)). Some functions may require you to be logged in to TikTok.

R users, check out [traktok](https://github.com/JBGruber/traktok), an R port of Pyktok.

**Installation**

```pip install pyktok``` (still a version behind but will fix soon)

**Requirements**

Pyktok relies on the following packages:

 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - [browser-cookie3](https://pypi.org/project/browser-cookie3/)
 - [Numpy](https://numpy.org/)
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)
 - [Selenium](https://pypi.org/project/selenium/)
 - [webdriver-manager](https://pypi.org/project/webdriver-manager/)

**Usage**

```python
import pyktok as pyk
```    
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
To download up to 30 metadata lines from a *user* page (note, for this to work you must set the `browser_name` parameter to a browser on your system that you have used to access TikTok *and* that is supported by `browser_cookie3`. I think the only valid values are `'chrome'` and `'firefox'`. Also you can get the videos too by setting `save_video` to `True`): 

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
To download all video comments initially visible on the page (previous versions of this function used TT's hidden API to capture many thousands of comments, but TT has disabled this feature, so the current function uses browser automation--which is unfortunately very slow--to pull only the comments that initially appear. However, you could use this function to download comments from videos periodically, which should give you a larger number of comments)
```python
pyk.save_visible_comments('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1')
```			

To download metadata for the keyword "funny" (practically speaking, you may not get all available data). This function has been rewritten since TT's data structure change, but should work. You can also download videos at the same time by setting `save_videos` to `True`. Also note that this endpoint sometimes delivers results based on keywords spelled similarly but unrelated to what you used (for example, the term "computational" also return matches for "computer" and "computing"). My only advice is to filter your data after the fact.
```python
pyk.save_tiktok_by_keyword('funny')
```

TikTok's servers may not love it if you run some of the above functions at full speed, so I recommend increasing the `sleep` parameter if you get autobanned. I haven't tested this extensively so I have no idea if or when autobans start to kick in.
