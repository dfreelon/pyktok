## Pyktok
**A simple module to collect video, text, and metadata from Tiktok.**

I developed Pyktok ("pick-tock") because none of the existing TikTok data collection utilities I could find worked for me. Pyktok pulls its data directly from the JSON object embedded in every Tiktok video and user page (except for `save_video_comments`, which uses the TikTok API). Here are its major features, most of which require the URL(s) of the content you wish to collect:

 - Download TikTok videos
 - Download video metadata
 - Download ~~up to 20 most recent~~ **all available video comments** (special thanks to **[@pkreissel](https://github.com/pkreissel)** for drafting the code for this!!!)
 - Download up to 30 most recent user video URLs
 - Download full TikTok JSON data objects (in case you want to extract data from parts of the object not included in the above functions)
 
This program may stop working suddenly if TikTok changes how it stores its data ([see Freelon, 2018](https://osf.io/preprints/socarxiv/56f4q/)).

**Installation**

```pip install pyktok```

**Requirements**

Pyktok relies on the following packages:

 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - [browser_cookie3](https://pypi.org/project/browser-cookie3/)
 - [Numpy](https://numpy.org/)
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)

**Usage**

```python
import pyktok as pyk
    
# download a single TikTok video and one line of metadata to the file "test_data.csv"
    
pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7106594312292453675?is_copy_url=1&is_from_webapp=v1',
	        True,
                video_data.csv')
    
# download another TikTok video and add its metadata to the same file as above
    
pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1',
	        True,
                'video_data.csv')
    
# get a list of URLs of up to 30 of a user's most recent videos
    
tiktok_videos = pyk.get_account_video_urls('https://www.tiktok.com/@tiktok')
    
#download metadata and comment data ONLY from video URLs collected via the preceding line of code (to also download the videos, change False to True). If TikTok autobans the scraper, try changing the 1 to a higher number to increase the number of seconds between executions.
    
pyk.save_tiktok_multi(tiktok_videos,
                      False,
                      'tiktok_data.csv',
                      1)
                         
#download an individual video's JSON object
	
tt_json = pyk.get_tiktok_json('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1')

#download all available video comments (this is the default behavior, but you can change the max_comments parameter if desired)

pyk.save_video_comments('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1',
			'chair_comments.csv')
			
#download all available video comments starting with comment #3865 (if your previous download session was interrupted; you can get the comment number from the console output)

pyk.save_video_comments('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1',
			'chair_comments.csv',
			cursor_resume=3865)
```

TikTok's servers may not love it if you run `save_tiktok_multi` or `save_video_comments` at full speed, so I recommend increasing the `sleep` parameter if you get autobanned. I haven't tested this extensively so I have no idea if or when autobans start to kick in.
