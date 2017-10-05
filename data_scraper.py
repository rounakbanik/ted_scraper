import requests
import bs4
import sys
import os
import time
import json
from pprint import pprint
import re

base_url = 'https://www.ted.com'
monster = []

def get_metadata(page_source):
	beg_index = page_source.find('<script>q("talkPage.init"')
	source = page_source[beg_index:]
	end_index = source.find(')</script>')
	script_tag = page_source[beg_index: beg_index + end_index]
	json_obj = script_tag[len('<script>q("talkPage.init", '): ]
	return json.loads(json_obj)


with open('urls.txt') as f:
	for count, url in enumerate(f):
		print("Requesting Talk Number: " + str(count))
		res = requests.get(url)
		try:
			res.raise_for_status()
		except:
			print("Time out. Waiting for 60 seconds")
			time.sleep(60)
			res = requests.get(url)
			res.raise_for_status()

		page_source = res.text
		metadata = get_metadata(page_source)
		metadata = metadata["__INITIAL_DATA__"]
		#print(metadata.keys())	

		talk_dict = {}
		talk_dict["comments"] = metadata["comments"]["count"]
		talk_dict["event"] = metadata["event"]
		talk_dict["description"] = metadata["description"]
		talk_dict["url"] = url
		talk_dict["name"] = metadata["name"]
		talk_dict["title"] = metadata["talks"][0]["player_talks"][0]["title"]
		talk_dict["film_date"] = metadata["talks"][0]["player_talks"][0]["filmed"]
		talk_dict["published_date"] = metadata["talks"][0]["player_talks"][0]["published"]
		talk_dict["main_speaker"] = metadata["talks"][0]["speaker_name"]
		talk_dict["num_speaker"] = len(metadata["speakers"])
		talk_dict["views"] = metadata["viewed_count"]
		talk_dict["languages"] = len(metadata["talks"][0]["downloads"]["languages"])
		talk_dict["duration"] = metadata["talks"][0]["duration"]
		talk_dict["ratings"] = metadata["talks"][0]["ratings"]
		talk_dict["tags"] = metadata["talks"][0]["player_talks"][0]["tags"]
		talk_dict["speaker_occupation"] = metadata["speakers"][0]["description"]
		talk_dict["related_talks"] = metadata["talks"][0]["related_talks"]

		"""
		transcript = ""
		transcript_res = requests.get(url + "/transcript")
		try:
			transcript_res.raise_for_status()
		except:
			print("Time out. Waiting for 25 seconds")
			time.sleep(25)
			transcript_res = requests.get(url + '/transcript')
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

		talk_dict['transcript'] = transcript
		"""
		
		monster.append(talk_dict)

json_file = open("ted_2017.json", 'w')
json_file.write(str(monster))
json_file.close()



