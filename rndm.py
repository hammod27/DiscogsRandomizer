#!/usr/bin/env python

import sys
import requests
import json
from random import randint

def main(usersList,numUsers):
	try:
		albumAndArtistList = []
		count = 0
		for userName in usersList:
			albumAndArtistList.append(getAlbumsFromApi(userName, albumAndArtistList))

		listSize = len(albumAndArtistList)
		randNum = randint(0,listSize - 2)

		print(albumAndArtistList[randNum])
	except Exception as e:
		if (userName == ""):
			print('Please enter at least one username.')
		else:
			print(userName + " is not a valid username.")

def getAlbumsFromApi(user, albumAndArtistList):
	url = 'http://api.discogs.com/users/{0}/collection/folders/0/releases?page=1&per_page=1000'.format(user)
	response = requests.get(url)
	#jsonText = response.json() #the next two lines replaced this. slightly faster?
	response.encoding = 'UTF-8'
	jsonText = json.loads(response.text)
	albumAndArtistList = buildAlbumList(jsonText, albumAndArtistList)
	return albumAndArtistList

def buildAlbumList(jsonText, albumAndArtistList):
	for i in jsonText['releases']:
		albumName = i['basic_information']['title']
		for j in i['basic_information']['artists']:
			artistName = j['name']
		albumAndArtist = albumName + " - " + artistName
		albumAndArtistList.append(albumAndArtist)
	return albumAndArtistList

def main2(users,numUsers):
	test = users.split(',')
	print(test[0])


users = sys.argv[1]
numUsers = sys.argv[2]

usersList = users.split(',')

main(usersList,numUsers)