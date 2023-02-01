import praw
import time
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("subreddit", help="Subreddit name to scrape")
parser.add_argument("header_name", help="Header name to search for in post titles")
parser.add_argument("--days", type=int, help="Number of days back in time to consider", default=30)
args = parser.parse_args()

reddit = praw.Reddit(client_id='<edit_this>',
                     client_secret='<edit_this>',
                     user_agent='<edit_this>')

def get_most_active_commenters(subreddit, header_name, days):
    comment_count = {}
    posts_found = 0
    users_helped = 0
    root_comments = 0
    total_time_delta = 0
    time_entries_count = 0
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
                root_comments += 1
                #If an originating comment has a response, consider that user helped
                if len(comment.replies) > 0:
                    users_helped += 1
                    time_delta = comment.replies[0].created_utc - comment.created_utc
                    total_time_delta += time_delta
                    time_entries_count += 1
                continue
            author = comment.author
            if author is None:
                continue
            if author.name in comment_count:
                comment_count[author.name] += 1
            else:
                comment_count[author.name] = 1
    if time_entries_count > 0:
        avg_time_delta = total_time_delta / time_entries_count
        avg_time_delta = avg_time_delta / 60    #minutes
        avg_time_delta = avg_time_delta / 60   #hours
    print(root_comments,users_helped)
    return comment_count,users_helped,avg_time_delta,(users_helped/root_comments)

subreddit = args.subreddit
header_name = args.header_name
days = args.days
most_active_commenters,num_helped,avg_time,percent_served = get_most_active_commenters(subreddit, header_name, days)

sorted_commenters = sorted(most_active_commenters.items(), key=lambda x: x[1], reverse=True)
top_10 = sorted_commenters[:10]
print()
print(f'In the last {days} days...')
print(f'{num_helped} users were helped ({percent_served:.2%}% overall), waiting an average of {avg_time:.2f} hours for a Mentor Response')
print(f'The total number of mentors active in that time was: {len(most_active_commenters)}')
print('The Most Active Mentors by Total Replies is:')
for key,value in top_10:
    print(f'{key}: {value}')


#print(most_active_commenters)
