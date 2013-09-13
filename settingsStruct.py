from os.path import dirname

"""
The settings struct that contains all paths and settings

\package settingsStruct
\file settingsStruct.py Settings Structure for parameter handling
\author David Engel (entrymissing@gmail.com)
\version 1.0
"""


class settingsStruct:
	"""
	A settings struct that can be generated from a file. Keys be accessed via the [] opertor. It is usable similar to a dict.
	
	The general structure of lines in the settings file is KEY - Value
	Empty lines and lines starting with # will be ignored
	
	General Usage is:

	>>> settings = settingsStruct('example.ini')
	>>> settings['CREATE']
	True
	
	The values true,false,yes and no will be returned as boolean
	Integer values will be returned as integers
	lists can be added by starting new lines with +
	
	\author David Engel (entrymissing@gmail.com)
	\version 1.0
	"""
	def __init__( self, settingsFile ):
		"""
		Constructor of the settingsStruct class. Loads the settings from a file by calling parseSettingsFile
	
		\param settingsFile A filename pointing to the file containing the settings. If the file does not exist it will throw a file not found exception.
		\author David Engel (entrymissing@gmail.com)
		\version 1.0
		"""
		#parse the settingsFile
		self.parseSettingsFile( settingsFile )
	
	def addKeyValuePair( self, key, value ):
		#if the key already exists we transform it into a list
		if key in self.settings:
			if isinstance(self.settings[key], list):
				self.settings[key].append(value)
			else:
				self.settings[key] = [self.settings[key], value]
		else:
			self.settings[key] = value

	def parseSettingsFile( self, settingsFile):
		"""
		Parse the settings file. For a well formed settings file confer demoSettings.ini
		
		Multiple calls to this function will overwrite previous settings. After calling the function values can be accesed via their keys
	
		\param settingsFile A filename pointing to the file containing the settings. If the file does not exist it will throw a file not found exception.
		\author David Engel (entrymissing@gmail.com)
		\version 1.0
		"""
		#init the settings dictonary
		self.settings = dict()

		#store the settings file
		self.settingsFile = settingsFile
		
		#store the basedirectory
		self.baseDirectory = dirname(settingsFile)

		#read the file
		with open(settingsFile, 'r') as fp:
			lines = fp.readlines()

		#set a flag that indicates whether we are dealing with a list parameter
		listFlag = False
		key = ''

		#cycle the lines
		for curLine in lines:
			#skip empty or comment lines
			if not curLine.strip() or curLine.startswith('#'):
				continue

			#strip away the plusses, they are only there for readability
			curLine = curLine.replace('+','').strip()
			
			#check if we have a key value pair
			if '=' in curLine:
				key,value = curLine.split('=',1)
				key = key.strip().lower()
				value = value.strip()

			#otherwise we are dealing with a continuation of a list
			else:
				value = curLine

			#check if the value is a bool
			if value.strip().lower() in ['yes','true']:
				self.addKeyValuePair(key, True)
				continue
			if value.strip().lower() in ['no','false']:
				self.addKeyValuePair(key, False)
				continue

			#check if it is a string value
			if value[0] == '"' and value[-1] == '"':
				value = value[1:-1]
				#add the baseDirectory where needed
				if not value.find('%BASEDIR%') == -1:
					value = value.replace('%BASEDIR%', self.baseDirectory)

				self.addKeyValuePair(key, value)
				continue

			#check if it is an integer value
			if value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
				self.addKeyValuePair(key, int(value))
				continue

			continue


	def getParam( self, key ):
		"""
		Retrieve a value for a key
		
		If the key is not in the dict an Exception will be raised
		booleans will be returned as bool
		Integers will be returend as ints
		Lists will be returned as lists
		Everything else will be returned as float
	
		\param key The key for which the value should be retrieved
		\author David Engel (entrymissing@gmail.com)
		\version 1.0
		"""
		#all keys are lowercase without trailing or leading whitespaces
		key = key.strip().lower()

		#check if the requested key exists
		if not key in self.settings:
			#throw an exception
			raise Exception('settingsStruct::getParam: Key \'' + key + ' not found error')

		#otherwise just return the key
		return self.settings[ key ]
	
	def __getitem__(self, key):
		return self.getParam(key)

