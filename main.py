import twitter
import io
import json
import pandas as pd
import os
import sys

from twitter.error import TwitterError
from time import sleep

pd.set_option('display.max_rows', 30*1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

filepath = os.path.dirname(sys.argv[0])

def PPrint():
	pass
# # review = list()

def print_line():
	print(3*' ', 77*'_', '\n')

class Destroyer(object):
	def __init__(self, api_key, api_secret_key, access_token, access_secret_token):
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
			with io.open(filepath + '/tweet.js', mode='r', encoding='utf-8') as tweetjs_file:
				tweets = json.loads(tweetjs_file.read()[25:])
		except FileNotFoundError:
			print(filepath)
			print (" -> Can't find tweet.js file.")
			print (" -> Please place the tweet.js file in the root directory")
			print('\n\n\n\n\n\n')
			sys.exit()
			pass

		return tweets

	def like_filter(self):
		try:
			likes = int (input(4*' '+'Enter Likes Limit: '))
		except ValueError:
			print("Error: Please enter a digit.")
			print("Please restart the program.")
			print("Exiting")
			print('\n\n\n')
			sys.exit()

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

		try:
			retweet_limit = int(input(4*' '+'Enter Retweets Limit: '))

		except ValueError:
			print("Error: Please enter a digit.")
			print("Please restart the program.")
			print("Exiting")
			print('\n\n\n')
			sys.exit()

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

		try:
			likes_limit = int (input(4*' '+'Enter Likes Limit: '))
			retweet_limit = int(input(4*' '+'Enter Retweets Limit: '))

		except ValueError:
			print("Error: Please enter a digit.")
			print("Please restart the program.")
			print("Exiting")
			print('\n\n\n')
			sys.exit()

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
		self.tweets_df.to_csv(filepath + '/review.csv')

	def delete_tweets(self):
		api_key = input("Please enter API key: ")
		api_secret_key = input("Please enter API secret key: ")
		access_token = input("Please enter Access token: ")
		access_secret_token = input("Please enter Access token secret: ")

		s = Destroyer(api_key, api_secret_key, access_token, access_secret_token)

		print(' -> Connecting with Twitter . . .')
		if s.verify():
			print(' -> Logged in as', s.get_name())
		else:
			print(' -> Login Failed!')
			print(' -> Bad credentials.')
			print(' -> Please re-check the credentials and Try again.')
			print_line()
			sys.exit()

		try:
			# Compile all the ids to be deleted in a list
			self.IDs = tp.tweets_df['ID'].tolist()
			# self.IDs = ['1202542001465507840', '1202524122552688640', '1202524067968016384','1202523895754055681', '1202540509031518208', '1202540488340967424', '1202540529508143110', '1202540529508143110']
		except KeyError:
			print("Empty list.")
			print("Please restart the program with different values.")
			print("Exiting")
			print('\n\n\n')
			sys.exit()

		print_line()

		one_last_time = input(4*" " + "One last time, Do you wish to continue (yes/no): ")

		print_line()

		if one_last_time.lower != 'yes':
			print(3*' ', 'Cool!')
			print(3* " ", "Exiting now")
			print('\n\n\n\n')
			sys.exit()

		for ID in self.IDs:

			try:
				tweet_text = s.api.GetStatus(ID).AsDict().get('text').replace('\n', ' \\n ')
				print(3	*' ', 'Deleteing:', tweet_text[:65])
				s.api.DestroyStatus(ID)

			except TwitterError:
				print(3*' ', 'Error: Tweet not found:', ID, )

			sleep(2)

		print()

if __name__=='__main__':
	os.system('clear')

	print(3*' ', 'Reading Tweets.js File . . .')
	print_line()

	tp = TweetsParser()

	print(' -> Note: Every tweet below the specified limit will be deleted.\n')

	while True:
		print(3*' ', 'Do you want to filter based on:')
		print(3*' ', ' a. Likes')
		print(3*' ', ' b. Retweets')
		print(3*' ', ' c. Both\n')

		option = input(4*' '+'Select Option (a, b or c): ')

		if option.lower() == 'a':
			print_line()

			tp.like_filter()
			break

		elif option.lower() == 'b':
			print_line()

			tp.retweet_filter()
			break

		elif option.lower() == 'c':
			print_line()

			tp.both_filter()
			break

		else:
			print(3*' ', 'Invalid input. Try typing "a", "b" or "c".\n')


	tp.set_dataframe()
	tp.make_csv()

	print()
	print(f' -> "review.csv" created with: {len(tp.review)} tweets.')
	print_line()



	while True:
		choice1 = input(4*' ' + 'Have you reviewed "review.csv" (yes/no): ')

		if choice1.lower() == 'yes':
			break
		else:
			print(' -> Please review "review.csv" to continue. \n')

	print_line()
	print(' -> Warning: This process is irreversible. Proceed with caution.\n')



	while True:
		choice2 = input(4*' '+'Are you sure, you want to delete all the tweets in "review.csv" (yes/no): ')

		if choice2.lower() == 'yes':
			print_line()

			tp.delete_tweets()

			print_line()
			print(22*' ', f'Successfully deleted: {len(tp.review)} Tweets.')
			print_line()

			break
		elif choice2.lower() == 'no':

			print_line()
			print(3*' ', 'Wise Decision ;-)')
			print_line()

			break
		else:
			print(3*' ', 'Invalid input. Try again.\n')
