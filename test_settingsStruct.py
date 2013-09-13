from settingsStruct import settingsStruct
from os import getcwd
from nose.tools import raises

def test_parameter_gettingString():
	settings = settingsStruct('example.ini')

	assert(settings['STRING_1'] == "A simple string")
	assert(settings['STRING_2'] == " Leading whitespaces are preserved")
	assert(settings['STRING_3'] == "Trailing whitespaces are preserved ")

def test_parameter_gettingBinary():
	settings = settingsStruct('example.ini')

	assert(settings['BINARY_YES'] == True)
	assert(settings['BINARY_NO'] == False)
	assert(settings['BINARY_TRUE'] == True)
	assert(settings['BINARY_FALSE'] == False)

def test_parameter_gettingInteger():
	settings = settingsStruct('example.ini')

	assert(settings['INTEGER_1'] == 1)
	assert(settings['INTEGER_20'] == 20)
	assert(settings['INTEGER_MINUS_3'] == -3)
	assert(settings['INTEGER_MINUS_40'] == -40)

def test_parameter_gettingList():
	settings = settingsStruct('example.ini')

	assert(len(settings['LISTPARAMETER1']) == 3)
	assert(settings['LISTPARAMETER1'][0] == 'String1')
	assert(settings['LISTPARAMETER1'][1] == 'String2')
	assert(settings['LISTPARAMETER1'][2] == 'String3')

	assert(len(settings['LISTPARAMETER2']) == 3)
	assert(settings['LISTPARAMETER2'][0] == 'String1')
	assert(settings['LISTPARAMETER2'][1] == 2)
	assert(settings['LISTPARAMETER2'][2] == True)

	assert(len(settings['LISTPARAMETER3']) == 2)
	assert(settings['LISTPARAMETER3'][0] == 1)
	assert(settings['LISTPARAMETER3'][1] == "String2")

	assert(len(settings['LISTPARAMETER4']) == 2)
	assert(settings['LISTPARAMETER4'][0] == False)
	assert(settings['LISTPARAMETER4'][1] == -2)

def  test_parameter_gettingBasedir():
	settings = settingsStruct('example.ini')

	assert(settings['BASEDIR'] == '')
	assert(settings['DATADIR'] == '/Data/')


def test_keys_case_insensitive():
	settings = settingsStruct('example.ini')

	assert(settings['BINARY_YES'] == settings['binary_yes'])
	assert(settings['INTEGER_MINUS_3'] == settings['integer_minus_3'])
	assert(settings['STRING_1'] == settings['stRinG_1'])

def test_nosurplus_parameters():
	settings = settingsStruct('example.ini')
	allParamters = "STRING_1","STRING_2","STRING_3","BINARY_YES","binary_no","binary_TRUE","BINARY_false","INTEGER_1","INTEGER_20","INTEGER_MINUS_3","INTEGER_MINUS_40","BASEDIR","DATADIR","LISTPARAMETER1","LISTPARAMETER2","LISTPARAMETER3","LISTPARAMETER4"

	assert(len(settings.settings) == len(allParamters))
	for curParam in allParamters:
		settings[curParam]

@raises(Exception)
def test_KeyError():
	settings = settingsStruct('example.ini')
	settings['NonExistingKey']

@raises(Exception)
def test_NonExistingFile():
	settings = settingsStruct('example_DoesNotExist.ini')




