#Pic Folder Cleaner
from os import listdir
from os.path import isfile, join
import os

path = 'knownPeople\\' 
files = [f for f in listdir(path) if isfile(join(path, f))]

for file in files:
	seperatorIndex = f.find('_')
	newFile = file[:seperatorIndex]
	os.rename(path + file, path + newFile + '.jpg')
