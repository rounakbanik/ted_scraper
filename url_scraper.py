import requests
import bs4
import sys
import os
import time

base_url = 'https://www.ted.com'
seed_url = 'https://www.ted.com/talks?sort=oldest&page='
urls = []

f = open('urls.txt', 'w')

for i in range(1,72):
	print("Downloading from page " + str(i))

	url = seed_url + str(i)
	res = requests.get(url)

	try:
		res.raise_for_status()
	except:
		print("Time out. Waiting for 25 seconds")
		time.sleep(25)
		res = requests.get(url)
		res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text)

	talkElem = soup.select('div.container.results div.col')
	print("Number of talks: " + str(len(talkElem)))

	for talk in talkElem:
		talk_url = base_url + talk.select('div.media__image a.ga-link')[0].get('href')
		urls.append(talk_url)
		f.write(talk_url + '\n')
		
		
print('Total number of talks: ' + str(len(urls)))
f.close()