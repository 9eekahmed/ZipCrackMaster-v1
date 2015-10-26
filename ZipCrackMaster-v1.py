#! /usr/bin/python3

import os
import time
from zipfile import *
from argparse import ArgumentParser

start_time = time.time()


HEADER = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WHITE = '\033[37m'
WARNING = '\033[93m'
FAIL = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'

class Crack:
	
	pwdTried=0
	FilesList=[]
	notFilesList=[]
	passFound=[]

	def __init__(self,a_filename,a_pwdList):
		self.FileName=a_filename
		self.pwdFile= a_pwdList

		self.__arrangeData()


	def __arrangeData(self):
		for items in self.FileName:
			if is_zipfile(items):
				self.FilesList.append(items)
			else:
				self.notFilesList.append(items)
		
		if len(self.FilesList) > 0:
			print(BOLD,WHITE,"Valid zip files to crack: ",ENDC,BLUE,self.FilesList,ENDC)
			print(BOLD,WHITE,"Invalid files: ",ENDC,FAIL,self.notFilesList,ENDC)

			self.__readPwdList()
		else:
			print(FAIL,"[*] ZipFiles not found !",ENDC)

	def __readPwdList(self):

		global start_time

		print(FAIL,"\nStart Cracking ...\n",ENDC)
		try:
			with open(self.pwdFile,'r') as pwdfile:
				while True:
					word = pwdfile.readline().strip()
					if word != '':
						self.pwdTried+=1
						self.__crack(bytes(word,'utf-8'))

						if len(self.FilesList) == 0:
							print(WHITE,"\n  Tested:",WARNING,self.pwdTried,WHITE," word !",ENDC)
							print('  Time: ',round(time.time()-start_time,2),'s')
							break
					else:
						if len(self.passFound) == 0:
							print(BOLD,FAIL,"\n[X] No match found ! -_-",ENDC)
						print(WHITE,"\n  Tested:",WARNING,self.pwdTried,WHITE," word !",ENDC)
						print('  Time: ',round(time.time()-start_time,2),'s')
						break
				

		except Exception as e:
			print("[X] ",str(e))

	def __crack(self,word):
		for each in self.FilesList:
			try:

				with ZipFile(each) as zfile:
					zfile.extractall(pwd=word)

				self.FilesList.remove(each)
				self.passFound.append(each)

				print(WHITE,"[*]",GREEN,each,":",word.decode(),ENDC)
								
			except:
				pass

def Main():
	
	print("==========================================================")
	print("  ZipCrackMaster | [Version]: 1.0")
	print("==========================================================")
	print("  [E-mail]: 9eek.mohamed@gmail.com | [Twitter]: @Geekm")
	print("==========================================================\n")
	
	parser = ArgumentParser()
	parser.add_argument('zipfile',help="Zip file name {file.zip} or list of zipfiles {file1.zip,file2.zip}", type=str)
	parser.add_argument('list', help="List of password to try it {pass.txt}",type=str)
	args=parser.parse_args()

	zipfiles=args.zipfile.split(',')
	pwdList=args.list


	run=Crack(zipfiles,pwdList)


if __name__ == '__main__':
	os.system('cls' if os.name == 'nt' else 'clear')
	Main()
