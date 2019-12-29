import os
import json
import datetime as dt

# Write, Get , create , delete (TO DO LIST)

#	Beginning -> create and write list onto the file 	//	Logger
#	Destination reached -> Remember second to last tag and request new path // rfid_reader 
#	OR on startup request on the parkingspot request new path // or when destination reached // validation on the rfid_reader

#	When end reached -> delete file // In rfid_reader file

class LocalFile:
	def __init__(self, name = "localinformation"):
			self.name = (name+'.txt')
			self.file = {}
			self.create_file()
			self.state = ['update','error','info', 'warning']


	def create_file(self):
		if os.path.isfile(self.name):
			open(self.name,'w')
		else:
			self.info("is created", self.name)
			open(self.name,'w+')

	def write_file(self, state , rfid_id):
		self.file[state] = []
		self.file[state].append({'date & time': str(dt.datetime.now().strftime('%d/%m/%y ---- %H:%M:%S'))})
		for i in range(len(rfid_id)):
			self.file[state].append({
				'rfid_tag': rfid_id[i] ,
			})
			with open(self.name,'w') as outfile:
				json.dump(self.file,outfile, indent= 2)

	def get_content(self, content):
		with open(self.name) as json_file:
			try:
				self.file = json.load(json_file)
				return self.file[str(content)]
			except:
				self.error(' does not exists', content)

	def clear_content(self):
		f = open(self.name, "w+")
		f.write('')
		f.close()

	def update(self, info, topic =''):
		print('[UPDATE]  ', topic, info)

	def info(self, info, topic =''):
		print('[INFO]    ', topic, info)

	def error(self, info, topic =''):
		print('[ERROR]   ', topic, info)