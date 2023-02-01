import praw
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("subreddit", help="Subreddit name to scrape")
parser.add_argument("header_name", help="Header name to search for in post titles")
parser.add_argument("--days", type=int, help="Number of days back in time to consider", default=30)
args = parser.parse_args()

reddit = praw.Reddit(client_id='<replace_this>',
                     client_secret='<replace_this>',
                     user_agent='<replace_this>')

def get_most_active_commenters(subreddit, header_name, days):
    comment_count = {}
    posts_found = 0
    for submission in reddit.subreddit(subreddit).new(limit=None):
        if time.time() - submission.created_utc > days*24*60*60:
            break
        #if header_name not in submission.title.lower():
        if header_name not in submission.title:
            continue
        else:
            posts_found += 1
            print(f'Found matching {posts_found} posts so far...')
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if comment.is_root:
                continue
            author = comment.author
            if author is None:
                continue
            if author.name in comment_count:
                comment_count[author.name] += 1
            else:
                comment_count[author.name] = 1

    return comment_count

subreddit = args.subreddit
header_name = args.header_name
days = args.days
most_active_commenters = get_most_active_commenters(subreddit, header_name, days)

sorted_commenters = sorted(most_active_commenters.items(), key=lambda x: x[1], reverse=True)
top_10 = sorted_commenters[:10]
print('The Most Active Mentors by Total Replies is:')
for key,value in top_10:
    print(f'{key}: {value}')


#print(most_active_commenters)
