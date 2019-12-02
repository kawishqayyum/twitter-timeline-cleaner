from selenium import webdriver
from time import sleep

url = "https://twitter.com/"

class DeleteTweets(object):
	
	def __init__(self, username, passw):
		
		self.driver = webdriver.Chrome("./chromedriver.exe")
		
		self.login(username, passw)
		self.driver.get(url + username)

		
	def login(self, username_, passw):
		
		self.driver.get(url + "login")

		sleep(1)

		username = self.driver.find_element_by_class_name('js-username-field.email-input.js-initial-focus')
		password = self.driver.find_element_by_class_name('js-password-field')
		login_b = self.driver.find_element_by_class_name('submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')

		username.send_keys(username_)
		password.send_keys(passw)

		login_b.click()
		sleep(3)

