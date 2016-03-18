import requests
import json 
from random import randint

def main():
	albumAndArtistList = []
	userList = []
	count = 0
	try:
		newAlbums = input('New or All records? Type \'New\' or \'All\'\n')
		
		howMany = int(input('how many users?\n'))
		while (count < howMany):
			tempVar = input('username?\n')
			userList.append(tempVar)
			count += 1

		if newAlbums == 'New' or newAlbums == 'new':
			numAlbums = int(input('Top how many albums?\n'))
			for user in userList:
			 	albumAndArtistList.append(getRecentAlbums(user, albumAndArtistList, numAlbums))
		elif newAlbums == 'All' or newAlbums == 'all':
			for user in userList:
			 	albumAndArtistList.append(getAlbumsFromApi(user, albumAndArtistList))
		else:
			raise ValueError('\'New\' or \'All\' wasn\'t typed in correctly')

		listSize = len(albumAndArtistList)
		randNum = randint(0,listSize)
		
		print(albumAndArtistList[randNum])
	except Exception as e:
		print('an error occurred :(\n')
		print( str(e))
	
def buildAlbumList(jsonText, albumAndArtistList):
	for i in jsonText['releases']:
		albumName = i['basic_information']['title']
		for j in i['basic_information']['artists']:
			artistName = j['name']
		albumAndArtist = albumName + " - " + artistName
		albumAndArtistList.append(albumAndArtist)
	return albumAndArtistList
	#idea: for {arbitrary random number} if it throws exception (indexOutOfBounds?) 
	#then lower the range of random ints and try again
	
def getAlbumsFromApi(user, albumAndArtistList):
	url = 'http://api.discogs.com/users/{0}/collection/folders/0/releases?page=1&per_page=1000'.format(user)
	response = requests.get(url)
	#jsonText = response.json() #the next two lines replaced this. slightly faster?
	response.encoding = 'UTF-8'
	jsonText = json.loads(response.text)
	albumAndArtistList = buildAlbumList(jsonText, albumAndArtistList)
	return albumAndArtistList

def buildRecentAlbumList(jsonText, albumAndArtistList, numAlbums):
	count = 0
	for i in jsonText['releases']:
		count += 1
		albumName = i['basic_information']['title']
		for j in i['basic_information']['artists']:
			artistName = j['name']
		albumAndArtist = albumName + " - " + artistName
		albumAndArtistList.append(albumAndArtist)
		if count >= numAlbums: break
	count = 0
	return albumAndArtistList

def getRecentAlbums(user, albumAndArtistList, numAlbums):
	url = 'http://api.discogs.com/users/{0}/collection/folders/0/releases?sort=added&sort_order=desc'.format(user)
	response = requests.get(url)
	jsonText = response.json()
	albumAndArtistList = buildRecentAlbumList(jsonText, albumAndArtistList, numAlbums)
	return albumAndArtistList

def getAlbumsFromApiQuicker(user, albumAndArtistList):
	url = 'http://api.discogs.com/users/{0}/collection/folders/0/releases?page=1&per_page=1000'.format(user)
	print("HERE")
	response = requests.get(url)
	response.encoding = 'UTF-8'
	jsonText = json.loads(response.text)
	albumAndArtistList = buildAlbumList(jsonText, albumAndArtistList)
	return albumAndArtistList

main()