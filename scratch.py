import requests
from bs4 import BeautifulSoup

# This is a dynamic or client side rendered page ehere it is always updated based on the new information if added/updated on that page.
youtube_trending_url = 'https://www.youtube.com/feed/trending'

# Does not execute JS
response = requests.get(youtube_trending_url)

with open('trending.html','w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text,'html.parser')
print(doc.title.text)

# Find the div in which video title is defined
video_div = doc.find_all('div',class_='text-wrapper style-scope ytd-video-renderer')
print(video_div)
