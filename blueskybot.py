from atproto import Client
import time
import requests
 
client = Client()
 
login = client.login('your_user.bsky.social','your_password')
print(login.handle,login.display_name,login.followers_count)

post = client.send_post('Hello, BlueSky!!! I\'m posting it using Python :)!')
 
 
## printing feed content
try:
    data = client.get_timeline(limit=30)
    feed = data.feed
    next_page = data.cursor
    for item in feed:
        print (item.post)
except NetworkError as error:
    print(f"something went wrong:{error} ")
 


## generous bot 
def limit_handler(follower_bundle):
    try:
        while True and len(follower_bundle.followers) > 0:
            yield follower_bundle.followers.pop()
    except NetworkError as error:
        time.sleep(1000)
 
followers = client.get_followers(login.did)
for follower in limit_handler(followers):
    # print(f"follower: {follower}")
    client.follow(follower.did)


 
## like bot 
search_string= 'Artificial Inteligence'
numberOfPosts = 2
count = 0
try:
    for item in feed:
       if item.post.record.text.find(search_string) > -1:
           count += 1
           client.like(item.post.uri, item.post.cid)
           if count >= numberOfPosts:
               break
except NetworkError as e:
    print(e.response)
except StopIteration as e:
    print(e)