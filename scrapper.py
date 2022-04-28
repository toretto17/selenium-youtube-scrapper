from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import pandas as pd

# This is a dynamic or client side rendered page ehere it is always updated based on the new information if added/updated on that page.
youtube_trending_url = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  
# Here we need to add the path of chromedriver where it is installed
  driver = webdriver.Chrome(options=chrome_options)
  print('driverrrrrrr',driver)
  return driver

def get_videos(driver):
  video_div_tag = 'ytd-video-renderer'
  driver.get(youtube_trending_url)
  video = driver.find_elements(By.TAG_NAME,value=video_div_tag)
  return video

def parse_video(video):
  title_tag = video.find_element(By.ID,'video-title')
  title = title_tag.text
  
  url = title_tag.get_attribute('href')
  
  thumbnail_url = video.find_element(By.TAG_NAME,'img').get_attribute('src')

  channel_div = video.find_element(By.CLASS_NAME,'style-scope ytd-channel-name')
  channel_name = channel_div.text

  video_view_posted_tag = video.find_element(By.ID,'metadata-line').text
  x = re.split('views\n',video_view_posted_tag)
  view = x[0]
  posted = x[1]

  description = video.find_element(By.ID,'description-text').text

  return {
    'title':title,
    'url':url,
    'thumbnail_url':thumbnail_url,
    'channel_name':channel_name,
    'view':view,
    'posted':posted,
    'description':description
  }


if __name__ == "__main__":
  print('creating driver')
  driver = get_driver()
  
  print('Fetching trending videos')
  video = get_videos(driver)
  print(len(video))

  # videos_data = [parse_video(x) for x in video]
  # for i in video:
  #   x= parse_video(i)
  #   print(x)
  videos_data = [parse_video(i) for i in video]
  print(videos_data)
  print()

  videos_df = pd.DataFrame(videos_data)
  print(videos_df)

  videos_df.to_csv('trending.csv',index=None)

  # title_tag = videos.find_element(By.ID,'video-title')
  # title = title_tag.text
  
  # url = title_tag.get_attribute('href')
  
  # thumbnail_url = videos.find_element(By.TAG_NAME,'img').get_attribute('src')

  # channel_div = videos.find_element(By.CLASS_NAME,'style-scope ytd-channel-name')
  # channel_name = channel_div.text

  # video_view_posted_tag = videos.find_element(By.ID,'metadata-line').text
  # x = re.split('views\n',video_view_posted_tag)
  # view = x[0]
  # posted = x[1]

  # description = videos.find_element(By.ID,'description-text').text
