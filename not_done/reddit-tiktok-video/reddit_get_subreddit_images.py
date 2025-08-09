import os
import urllib
import requests
import praw


reddit = praw.Reddit (
    username= "test",
    password= "pass",
    client_id="take_from_reddit_api",
    client_secret="take_from_reddit_api",
    user_agent="Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
)
#idee: video-uri cu privelisti si pus imagine cu traps pentru cateva milisecunde

#telegram
# 29069371
# c5afc7f077df2e4681aaaf262ff8e545

submission = reddit.submission(url="")
subreddit_names = ['Subbredit']
#GodPussy, Innie, GodPussy, BEAUTIFULPUSSY, vagina, RealGirls, collegesluts, ChristianGirls, barelylegalteens, xsmallgirls
#GirlsGW, EmoGirlsFuck, OnlyFans101, lingerie, Babes, Busty_Girls, PunkGirls, OnlyFansPromotions, YoungGirlsGoneWild
#Pussy_Perfection, Ratemypussy, GothPussy, AdorableNudes. Nudes, Nude_Selfie, EbonyGirls, EbonyCuties, Ebony. PetiteGoneWild
# GirlsNude, simps, ginger, redheads, bodyperfection, LatinasGW, asstastic (x3), palegirls, BubbleButts, ass, SmallCutie
#suicidegirls

# Iterate through each subreddit
for subreddit_name in subreddit_names:
    # Retrieve the last 25 videos and images from the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.top(limit=1000, time_filter='month')  # 'all' = all-time / year /month

    # Create the folders for the subreddit if it doesn't already exist
    #video_path = f'{subreddit_name}/videos/'
    post_path = f'{subreddit_name}/images/'
    #if not os.path.exists(video_path): os.makedirs(video_path)
    if not os.path.exists(post_path): os.makedirs(post_path)
    #start iterating at the 150th image
    posts = list(posts)

    # Download and save the videos and images
    last_upvotes= 10000000
    title_image = subreddit_name
    for idx,post in enumerate(posts):

        url = post.url
        title = post.title
        upvotes = post.ups
        print(url, title, upvotes)

        # Modify the title to make it a valid file name
        if not os.path.isabs(title):
            title = title.replace(' ', '_')
            title = title.replace('/', '_')
            title = title.replace('\\', '_')
            title = title.replace(':', '_')
            title = title.replace('*', '_')
            title = title.replace('?', '_')
            title = title.replace('"', '_')
            title = title.replace('<', '_')
            title = title.replace('>', '_')
            title = title.replace('|', '_')

        # Check the file extension to determine if it's an image or a video
        if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'):
            response = requests.get(url)
            # Specify the path to the file in the folder
            #file_path = os.path.join(post_path, f'{upvotes}_{title}.jpg')
            if last_upvotes == upvotes:
                # If the last upvotes are the same, append the index to the filename
                file_path = os.path.join(post_path, f'{upvotes}_{idx}_{title_image}.jpg')
            file_path = os.path.join(post_path, f'{upvotes}_{title_image}.jpg')
            # Save the file to the specified path
            open(file_path, 'wb').write(response.content)

        # if post.is_video:
        #     video_url = post.media['reddit_video']['fallback_url']
        #     response = requests.get(video_url)
        #
        #     # Specify the path to the file in the folder
        #     file_path = os.path.join(video_path, f'{upvotes}_{title}.mp4')
        #     # Save the file to the specified path
        #     open(file_path, 'wb').write(response.content)
        last_upvotes = upvotes
