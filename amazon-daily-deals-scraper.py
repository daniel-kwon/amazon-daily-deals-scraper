# import libraroes
import csv

import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re
from datetime import date


# url specification
websiteUrl = 'https://www.amazon.ca/gp/goldbox'

with open('amazon_daily_deals_'+ str(date.today()) +'.csv', mode='w') as amazon_daily_deals_file:
	amazon_daily_deals_writer = csv.writer(amazon_daily_deals_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	driver = webdriver.Chrome('C:/Users/danie/Documents/Python/chromedriver.exe') 
	# driver.implicitly_wait(10) # seconds
	driver.get(websiteUrl)

	while len(driver.find_elements_by_xpath('//div[@id="FilterItemView_page_pagination"]/div/span/div/ul/li/a[@href="#next"]')) > 0:
		parentProductDiv = driver.find_element_by_id('widgetContent')
		numberOfProducts = int(parentProductDiv.get_attribute('childElementCount'))
		for i in range(numberOfProducts):
			dealTitle = ''
			dealUrl = ''
			price = ''
			oldPrice = ''
			rating = ''
			reviewNumber = ''
			shipSoldInfo = ''
			try:
				price = driver.find_element_by_xpath('//*[@id="100_dealView_' + str(i) +'"]/div/div[2]/div/div/div[3]/div/span').get_attribute('innerText')
			except NoSuchElementException:
				pass
			try:
				oldPrice = driver.find_element_by_xpath('//*[@id="100_dealView_' + str(i) +'"]/div/div[2]/div/div/div[3]/div[2]/span[2]').get_attribute('innerText')
			except NoSuchElementException:
				pass
			try:
				dealTitle = driver.find_element_by_xpath('//*[@id="100_dealView_' + str(i) +'"]/div/div/div/div/div/a[@id="dealTitle"]/span').get_attribute('innerText')
			except NoSuchElementException:
				pass
			try:
				dealUrl = driver.find_element_by_xpath('//*[@id="100_dealView_' + str(i) +'"]/div/div/div/div/div/a[@id="dealTitle"]/a').get_attribute('href')
			except NoSuchElementException:
				pass
			try:
				reviewNumber = driver.find_element_by_xpath('//*[@id="100_dealView_' + str(i) + '"]/div/div[2]/div/div/div[7]/div/a/span/span').get_attribute('innerText')
			except NoSuchElementException:
				pass
			try:
				shipSoldInfo = driver.find_element_by_xpath('//*[@id="100_dealView_'+ str(i) + '"]//span[@id="shipSoldInfo"]').get_attribute('innerText')
			except NoSuchElementException:
				pass
			try:
				ratingArray = re.split('a-star-',driver.find_element_by_xpath('//*[@id="100_dealView_'+ str(i) + '"]/div/div[2]/div/div/div[9]/div/a/span/i').get_attribute('className'))
				rating = ratingArray[1].replace('-','.')
			except NoSuchElementException:
				pass
			amazon_daily_deals_writer.writerow([dealTitle,dealUrl,price,oldPrice,rating,reviewNumber,shipSoldInfo])

		next_button = driver.find_element_by_xpath('//div[@id="FilterItemView_page_pagination"]/div/span/div/ul/li/a[@href="#next"]')
		driver.execute_script("arguments[0].scrollIntoView();", next_button)
		

	driver.quit()