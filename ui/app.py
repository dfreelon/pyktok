# You can run the streamlit as follows: streamlit run ui/app.py

import streamlit as st
import pyktok as pyk


st.set_page_config(page_title="Pyktok Streamlit app")

# Choose browser
browser_options = ['Chrome', 'Firefox']
browser_choice = st.selectbox('Choose your preferred browser:', browser_options)

# Set options for pyktok
browser_name = 'chrome' if browser_choice == 'Chrome' else 'firefox'

options = {
    'download_single_video': 'To download a single TikTok video and one line of metadata to the file "video_data.csv"',
    'download_metadata': 'To download metadata ONLY from the video URLs used in the preceding two lines of code',
    'download_user_page': 'To download up to 30 metadata lines from a user page',
    'download_hashtag_page': 'To download up to 15 metadata lines from a hashtag page',
    'download_music_page': 'To download up to 15 metadata lines from a music page',
    'download_comments': 'To download all video comments initially visible on the page',
    'download_comments_multiple_videos': 'To download visible comments from multiple videos at the same time'
}

selected_option = st.selectbox("Please select the option you would like to use", list(options.values()))

# Get the corresponding key of the selected value
selected_key = [key for key, value in options.items() if value == selected_option][0]


from urllib.parse import urlparse

def is_tiktok_url(url):
    """
    Check if the given URL is a valid TikTok URL.

    Parameters:
    url (str): The URL to check

    Returns:
    bool: True if the URL is a TikTok URL, False otherwise.
    """
    parsed_url = urlparse(url)
    return parsed_url.hostname in ('www.tiktok.com', 'tiktok.com')

if selected_key == 'download_single_video':
    single_tt_vid_url = st.text_input('Enter the URL of the video: ')
    if not single_tt_vid_url:
        st.write("Error: Empty URL")
    elif not is_tiktok_url(single_tt_vid_url):
        st.write("Error: Not a valid TikTok URL")
    else:
        pyk.save_tiktok(single_tt_vid_url, True, 'video_data.csv',  browser_name)


elif selected_key == 'download_metadata':
    multi_tt_urls = st.text_input('Enter the URLs of the videos separated by a comma: ', )
    if not multi_tt_urls:
        st.write("Error: Empty URL")

    else:
        multi_tt_url_list = [url.strip() for url in multi_tt_urls.split(',') if is_tiktok_url(url.strip())]
        if not multi_tt_url_list:
            st.write("Error: No valid TikTok URLs found")
        else:
            include_video_download =  st.radio( "Do you want to download the videos too?", ('No', 'Yes'), horizontal=True)
            pyk.save_tiktok_multi_urls(multi_tt_url_list, include_video_download == 'Yes', 'tiktok_data.csv', 1)

elif selected_key in ('download_user_page', 'download_hashtag_page', 'download_music_page'):
    tt_multipage_url = st.text_input("Enter the URL:")
    if not tt_multipage_url:
        st.write("Error: Empty URL")
    elif not is_tiktok_url(tt_multipage_url):
        st.write("Error: Not a valid TikTok URL")
    else:
        save_video = st.radio("Do you want to download the video?", ('No', 'Yes'))
        pyk.save_tiktok_multi_page(tt_multipage_url, save_video=='Yes', save_metadata=True, browser_name=browser_name)


elif selected_key in ('download_comments', 'download_comments_multiple_videos'):
    tt_visible_comments_str = st.text_input("Enter the URLs of the videos separated by a comma:")
    if not tt_visible_comments_str:
        st.write("Error: Empty URL")
    else:
        tt_visible_comments_list = [url.strip() for url in tt_visible_comments_str.split(',') if is_tiktok_url(url.strip())]
        if not tt_visible_comments_list:
            st.write("Error: No valid TikTok URLs found")




