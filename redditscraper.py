import feedparser
import praw
import pandas as pd
import pprint
import re


# create connection with API
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='//insert_client_id//', client_secret="//insert_client_secret//")

def clean_text(rgx_match, text):
    new_text = text
    new_text = re.sub(rgx_match, '', new_text)
    return new_text


# get top 10 from reddit.com
d = feedparser.parse('http://www.reddit.com/.rss')

l = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []
l7 = []
l8 = []
l9 = []
l10 = []

num_of_entries = len(d['entries'])

for i in range(0, num_of_entries):
    l.append(d['entries'][i]['link'] )
    l2.append(d['entries'][i]['tags'][0]['term'].encode('ascii', 'ignore'))
    m = re.search('<div[^>]*>(.*)</div>', d['entries'][i]['summary'])
    if m:
        found = m.group(1)
    else:
        found = ''

    clean = clean_text('<[^>]*>', found)
    l3.append(clean)
    submission = reddit.submission(url=l[i])
    l4.append(submission.title)
    l5.append(submission.id)
    l6.append(submission.score)
    l7.append(d['entries'][2]['updated'])
    l8.append(submission.num_comments)
    l9.append(submission.ups)
    l10.append(submission.downs)

d1 = {'link': l, 'subreddit': l2, 'body': l3, 'title': l4, 'id': l5, 'score': l6, 'date':l7, 'comment_count':l8, 'ups':l9, 'downs':l10}
df1 = pd.DataFrame(data=d1)
df_json = df1.to_json(path_or_buf= '//insert_file_path//.json',)


for x in range(0, len(l)):
    submission = reddit.submission(url=l[x])
    # create list with data
    if hasattr(submission, 'id'):
        article_title = submission.title
        article_id = submission.id
        article_score = submission.score

    id_list = []
    body_list = []
    score_list = []
    permalink_list = []
    created_utc_list = []
    link_id_list = []

    y = len(submission.comments)

    for i in range(0, y):
        if hasattr(submission.comments[i], 'body'):
            id_list.append(submission.comments[i].id)
            body_list.append(submission.comments[i].body)
            score_list.append(submission.comments[i].score)
            permalink_list.append(submission.comments[i].permalink)
            created_utc_list.append(submission.comments[i].created_utc)
            link_id_list.append(submission.comments[i].link_id)

    d = {'article_title': article_title, 'article_id': article_id, 'article_score': article_score, 'id': id_list, 'body': body_list, 'score': score_list, 'permalink': permalink_list,  'created_utc':created_utc_list,
    'link_id':link_id_list}
    df = pd.DataFrame(data=d)
    df_json = df.to_json(path_or_buf= '//insert_file_path//'+str(x)+'.json',)
