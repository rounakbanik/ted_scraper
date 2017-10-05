import requests
import bs4
import sys
import os
import time
import json
from pprint import pprint
import re

base_url = 'https://www.ted.com'
json_file = open('transcripts_2017.json', 'a')
monster = []

#json_file.write('[ ')

with open('urls.txt') as f:
	for count, url in enumerate(f):
		if count >= 1983:
			print("Requesting Transcript Number: " + str(count))
			
			talk_dict = {}
			talk_dict["url"] = url

			
			transcript = ""
			transcript_res = requests.get(url + '/transcript')

			if transcript_res.status_code == 404:
				talk_dict["transcript"] = ""
				monster.append(talk_dict)
				print("No transcrpit found. Moving to next URL.")
				continue

			try:
				transcript_res.raise_for_status()
			except:
				print("Time out. Waiting for 60 seconds")
				time.sleep(60)
				transcript_res = requests.get(url + '/transcript')
				print(transcript_res.headers)
				transcript_res.raise_for_status()

			soup = bs4.BeautifulSoup(transcript_res.text)
			transElem = soup.select('div.Grid.Grid--with-gutter.p-b:4')
			print(len(transElem))

			for piece in transElem:
				classes = piece.get('class')
				#print(piece)
				text = piece.select('p')[0].text
				text = text.strip()
				transcript = transcript + text
				transcript = re.sub('\t', '', transcript)
				transcript = re.sub('\n', ' ', transcript)

			talk_dict["transcript"] = transcript
		
			json_file.write(str(talk_dict) + ", ")
			monster.append(talk_dict)


json_file.write(' ]')
json_file.close()



