## Pyktok
**A simple module to collect video, text, and metadata from Tiktok.**

I developed Pyktok ("pick-tock") because none of the existing TikTok data collection utilities I could find worked for me. Because TikTok's official API does not permit data extraction, Pyktok pulls its data directly from the JSON object embedded in every Tiktok video and user page. Here are its major features, most of which require the URL(s) of the content you wish to collect:

 - Download TikTok videos
 - Download video metadata
 - Download up to 20 most recent video comments
 - Download up to 30 most recent user video URLs
 - Download full TikTok JSON data objects (in case you want to extract data from parts of the object not included in the above functions)
 
This program may stop working suddenly if TikTok changes how it stores its data ([see Freelon, 2018](https://osf.io/preprints/socarxiv/56f4q/)).
 
**Requirements**

Pyktok relies on the following packages:

 - [browser_cookie3](https://pypi.org/project/browser-cookie3/0.6.0/)
 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - [Numpy](https://numpy.org/)
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)

**Usage**

```python
    import pyktok as pyk
    
    # download a single TikTok video and one line of metadata to the file "test_data.csv"
    
    pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7106594312292453675?is_copy_url=1&is_from_webapp=v1',
                    True,
                    'video_data.csv')
    
    # download another TikTok video, add its metadata to the same file as above, and create a new file containing comment data
    
    pyk.save_tiktok('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1',
                    True,
                    'video_data.csv',
                    'comment_data.csv')
    
    # get a list of URLs of up to 30 of a user's most recent videos
    
    tiktok_videos = pyk.get_account_video_urls('https://www.tiktok.com/@tiktok')
    
    #download metadata and comment data ONLY from video URLs collected via the preceding line of code (to also download the videos, change False to True). If TikTok autobans the scraper, try changing the 0 to a higher number to increase the number of seconds between executions.
    
    pyk.save_tiktok_multi(tiktok_videos,
                          False,
                          'tiktok_data.csv',
                          'tiktok_comments.csv',
                          0)
                         
	#download an individual video's JSON object
	
	tt_json = pyk.get_tiktok_json('https://www.tiktok.com/@tiktok/video/7011536772089924869?is_copy_url=1&is_from_webapp=v1')
```
Obviously it'd be great if Pyktok could pull more than 30 user videos and 20 comments, but that would likely involve browser emulation, which is not a can of worms I intend to open anytime soon.

TikTok's servers may not love it if you run `save_tiktok_multi` at full speed, so I recommend increasing the `sleep` parameter (the 0 in the example above) if you get autobanned. I haven't tested this extensively so I have no idea if or when autobans start to kick in.
