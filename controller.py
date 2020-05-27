# Top level control for Door Cam
import cv2
import face_recognition
import datetime
from os import listdir
from os.path import isfile, join
import pygame
import random
import time
import json
nextPlay = datetime.datetime.now()

def playSong(person):
	if not(person == 'Unknown') and checkCoolDown(person) and isActive():
		audioPath = 'audioClips\\' + person + '\\'
		try:
			files = [f for f in listdir(audioPath) if isfile(join(audioPath, f))]
			print(f'Hello {person}!')
			if len(files) > 0:
				audioFile = files[0]
				if len(files) > 1:
					audioIndex = random.randint(0, len(files) - 1)
					audioFile = files[audioIndex]
				print(f'Playing {audioFile}')
				pygame.mixer.music.load(audioPath + audioFile)
				pygame.mixer.music.set_volume(1.0)
				pygame.mixer.music.play()
		except:
			print(f'Error Playing Song for {person}')

def checkCoolDown(person):
	if person == 'Justin' or person == 'John' or person == 'Brett':
		coolDown = datetime.timedelta(minutes = 3)
	else:
		coolDown = datetime.timedelta(minutes = 3)

	if person in coolDict:
		if datetime.datetime.now() > coolDict[person]: #10 mins
			coolDict[person] = datetime.datetime.now() + coolDown
			print(f'Next song for {person} will be available at {coolDict[person]}')
			return True
	else:
		coolDict.update({person:datetime.datetime.now() + coolDown})
		print(f'Next song for {person} will be available at {coolDict[person]}')
		return True
	print(f'Next song for {person} will be available at {coolDict[person]}')
	return False


def isActive():
	now = datetime.datetime.now()#2018-11-06 11:37:24.164875
	day = datetime.datetime.today().weekday() #monday: 0 - Sunday: 6

	if disableOverRide:
		print('Currently Disabled')
		return False

	if day == 5: #saturday
		return not(now > now.replace(hour=weekendQuietStart[0], minute=weekendQuietStart[1]) and now < now.replace(hour=weekendQuietEnd[0], minute=weekendQuietEnd[1])) 
	#shuts off saturday 2:30 am to 10:30 am
	elif day == 4: #friday
		return now > now.replace(hour=weekStartTime[0], minute=weekStartTime[1])
	elif day == 6: #sunday
		return not(now > now.replace(hour=weekendQuietStart[0], minute=weekendQuietStart[1]) and now < now.replace(hour=weekendQuietEnd[0], minute=weekendQuietEnd[1])) and now < now.replace(hour=weekEndTime[0], minute=weekEndTime[1])
	else: 
		return now > now.replace(hour=weekStartTime[0], minute=weekStartTime[1]) and now < now.replace(hour=weekEndTime[0], minute=weekEndTime[1])
	

pygame.init()
pygame.mixer.init()

weekStartTime = [10, 30, 00]

weekEndTime = [22, 30, 00] # 10: 30 pm
coolDict = {}
weekendQuietStart = [2, 30, 00]

weekendQuietEnd = weekStartTime

disableOverRide = False # add disable button


known_face_encodings = []
known_face_names = []

video_capture = cv2.VideoCapture(0)
peoplePath = 'knownPeople\\' 
files = [f for f in listdir(peoplePath) if isfile(join(peoplePath, f))]
for file in files:
	personImage = face_recognition.load_image_file(peoplePath + file)
	personFaceEncoding = face_recognition.face_encodings(personImage)[0]
	known_face_encodings.append(personFaceEncoding)
	known_face_names.append(file[:-4])#truncate .jpg

face_locations = []
face_encodings = []
face_names = []

processFrame = True
currentPerson = ''

while True:
	ret, frame = video_capture.read()
	smallFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
	rgbSmallFrame = smallFrame[:, :, ::-1]

	if processFrame:
		face_locations = face_recognition.face_locations(rgbSmallFrame)
		face_encodings = face_recognition.face_encodings(rgbSmallFrame, face_locations)

		face_names = []
		for faceEncoding in face_encodings:
			matches = face_recognition.compare_faces(known_face_encodings, faceEncoding)
			name = 'Unknown'
			if True in matches:
				firstMatchIndex = matches.index(True)
				name = known_face_names[firstMatchIndex]
			face_names.append(name)
	processFrame = not processFrame
	if True: #if door opens 
		if len(face_names) > 0:
			#print(face_names[0])
			if datetime.datetime.now() > nextPlay:
				nextPlay = datetime.datetime.now() + datetime.timedelta(seconds = 10) 
				playSong(face_names[0])

	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	with open('config.json') as config:
		settings = json.load(config)
	disableOverRide = data['DisableOverride']



video_capture.release()
cv2.destroyAllWindows()
