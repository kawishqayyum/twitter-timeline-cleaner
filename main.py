import twitter
import io
import json
import pandas as pd
import os

pd.set_option('display.max_rows', 30000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

review = list()

def delete_tweets():
	pass

with io.open('./tempered.js', mode='r', encoding='utf-8') as tweetjs_file:
	tweets = json.loads(tweetjs_file.read()[25:])

os.system('clear')

print('\n\n\nNote: Everything below the cut-off limit will be deleted.\n')

retweet_limit = int(input('Enter Cut-off limit for retweets :'))
likes_limit = int (input('Enter Cut-off limit for likes    :'))

for tweet in tweets:
	
	if int(tweet.get('favorite_count')) > likes_limit:
		tweetD = dict()

		tweetD['ID'] = tweet.get('id')
		tweetD['Text'] = tweet.get('full_text')
		tweetD['Likes'] = tweet.get('favorite_count')
		tweetD['Retweets'] = tweet.get('retweet_count')
		tweetD['Time'] = tweet.get('created_at')

		review.append(tweetD)

tweets_df = pd.DataFrame(review)
tweets_df.to_csv('./review.csv')

print('\n\n*** Warning: This process is irreversible. Please roceed with caution. ***\n\n')

choice = input('Are you sure, you want to delete all the tweets in review.csv (yes/no): ')

if choice.lower() == 'yes':
	delete_tweets()
elif choice.lower() == 'no':
	print('Wise Decision ;-)')
else:
	print("Incorrect input")


print('Hahahahah hahahahahahah :)')
# display(tweets_df)

