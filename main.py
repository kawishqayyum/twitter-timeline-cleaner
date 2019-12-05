import twitter
import io
import json
import pandas as pd
import os
import sys

from twitter.error import TwitterError
from user_data import *
from time import sleep

pd.set_option('display.max_rows', 30*1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

def PPrint():
	pass
# # review = list()

class Destroyer(object):
	def __init__(self):
		self.api = twitter.Api(consumer_key=api_key, consumer_secret=api_secret_key, access_token_key=access_token, access_token_secret=access_secret_token)


	def verify(self):
		try:
			self.api.VerifyCredentials()
			return True
		except TwitterError:
			return False

	def get_name(self):
		return self.api.VerifyCredentials().AsDict().get('screen_name')



		
class TweetsParser(object):
	def __init__(self):
		self.tweets = self.get_tweets()
		self.review = list()
		self.tweets_df = pd.DataFrame()
		self.IDs = list()

	def get_tweets(self):
		
		try:
			with io.open('./tweet.js', mode='r', encoding='utf-8') as tweetjs_file:
				tweets = json.loads(tweetjs_file.read()[25:])
		except FileNotFoundError:
			print()
			print ("Can't find tweet.js file.")
			print ("Please place the tweet.js file in the root directory")
			sys.exit()
			pass

		return tweets

	def like_filter(self):
		
		likes = int (input(4*' '+'Enter Likes Limit: '))

		for tweet in self.tweets:
			if int(tweet.get('favorite_count')) < likes:
				tweetD = dict()

				tweetD['ID'] = tweet.get('id')
				tweetD['Text'] = tweet.get('full_text')
				tweetD['Likes'] = tweet.get('favorite_count')
				tweetD['Retweets'] = tweet.get('retweet_count')
				tweetD['Time'] = tweet.get('created_at')

				self.review.append(tweetD)

	def retweet_filter(self):

		retweet_limit = int(input(4*' '+'Enter Retweets Limit: '))

		for tweet in self.tweets:
			if int(tweet.get('favorite_count')) < retweet_limit:
				tweetD = dict()

				tweetD['ID'] = tweet.get('id')
				tweetD['Text'] = tweet.get('full_text')
				tweetD['Likes'] = tweet.get('favorite_count')
				tweetD['Retweets'] = tweet.get('retweet_count')
				tweetD['Time'] = tweet.get('created_at')

				self.review.append(tweetD)

	def both_filter(self):

		likes_limit = int (input(4*' '+'Enter Likes Limit: '))
		retweet_limit = int(input(4*' '+'Enter Retweets Limit: '))
		
		for tweet in self.tweets:
			if int(tweet.get('favorite_count')) < likes_limit and int(tweet.get('favorite_count')) < retweet_limit:
				tweetD = dict()

				tweetD['ID'] = tweet.get('id')
				tweetD['Text'] = tweet.get('full_text')
				tweetD['Likes'] = tweet.get('favorite_count')
				tweetD['Retweets'] = tweet.get('retweet_count')
				tweetD['Time'] = tweet.get('created_at')

				self.review.append(tweetD)

	def set_dataframe(self):
		self.tweets_df = pd.DataFrame(self.review)

	def make_csv(self):
		self.tweets_df.to_csv('./review.csv')

	def delete_tweets(self):
		s = Destroyer()

		print(' -> Connecting with Twitter . . .')
		if s.verify():
			print(' -> Logged in as', s.get_name())
		else:
			print('Login Failed!')

		# Compile all the ids to be deleted in a list
		self.IDs = tp.tweets_df['ID'].tolist()

		print(3*' ', 77*'_', '\n')
		
		for id in self.IDs[:10]:
			
			tweet_text = s.api.GetStatus(id).AsDict().get('text').replace('\n', ' \\n ')
			
			print(3*' ', 'Deleteing:', tweet_text[:65], end='\r', flush=True)
			sleep(2)

		print()

if __name__=='__main__':
	os.system('clear')
	
	print(3*' ', 'Reading Tweets.js File . . .')
	print(3*' ', 77*'_', '\n')

	tp = TweetsParser()

	print(' -> Note: Every tweet below the specified limit will be deleted.\n')
	
	while True:
		print(3*' ', 'Do you want to filter based on:')
		print(3*' ', ' a. Likes')
		print(3*' ', ' b. Retweets')
		print(3*' ', ' c. Both\n')

		option = input(4*' '+'Select Option (a, b or c): ')

		if option.lower() == 'a':
			print(3*' ', 77*'_', '\n')

			tp.like_filter()
			break

		elif option.lower() == 'b':
			print(3*' ', 77*'_', '\n')

			tp.retweet_filter()
			break

		elif option.lower() == 'c':
			print(3*' ', 77*'_', '\n')
			
			tp.both_filter()
			break
		
		else:
			print(3*' ', 'Invalid input. Try typing "a", "b" or "c".\n')


	tp.set_dataframe()
	tp.make_csv()

	print()
	print(f' -> "review.csv" created with: {len(tp.review)} tweets.')
	print(3*' ', 77*'_', '\n')

	while True:
		choice1 = input(4*' ' + 'Have you reviewed "review.csv" (yes/no): ')

		if choice1.lower() == 'yes':
			break
		else:
			print(' -> Please review "review.csv" to continue. \n')

	print(3*' ', 77*'_', '\n')
	print(' -> Warning: This process is irreversible. Proceed with caution.\n')

	while True:
		choice2 = input(4*' '+'Are you sure, you want to delete all the tweets in "review.csv" (yes/no): ')

		if choice2.lower() == 'yes':
			print(3*' ', 77*'_', '\n')

			tp.delete_tweets()
			
			print(3*' ', 77*'_', '\n')
			print(22*' ', f'Successfully deleted: {len(tp.review)} Tweets.')
			print(3*' ', 77*'_', '\n')
			
			break
		elif choice2.lower() == 'no':
			
			print(3*' ', 77*'_', '\n')
			print(3*' ', 'Wise Decision ;-)')
			print(3*' ', 77*'_', '\n')
			
			break
		else:
			print(3*' ', 'Invalid input. Try again.\n')