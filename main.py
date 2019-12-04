import twitter
import io
import json
import pandas as pd

review = list()

with io.open('./tempered.js', mode='r', encoding='utf-8') as tweetjs_file:
	tweets = json.loads(tweetjs_file.read()[25:])

likes_limit = int(input('Enter Cut-off limit for retweets :'))
retweet_limit = int (input('Enter Cut-off limit for likes    :'))

for tweet in tweets:
	
	if int(tweet.get('favorite_count')) > likes_limit:
		tweetD = dict()

		tweetD['ID'] = tweet.get('id')
		tweetD['Text'] = tweet.get('full_text')
		tweetD['Likes'] = tweet.get('favorite_count')
		tweetD['Retweets'] = tweet.get('retweet_count')
		tweetD['Time'] = tweet.get('created_at')

		review.append(tweetD)


pd.set_option('display.max_rows', 30000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

tweets_df = pd.DataFrame(review)
display(tweets_df)

