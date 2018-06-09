#!/usr/bin/python    

import sys
import requests
import datetime
import os
import json


########################################################################

build_configuration = 'Staging'
host = 'https://srvm.tutk.com/'

########################################################################


def get_catalog():

	catalog = ['P2PDVRLive', 'Kalay Box', 'PCX Inside', 'P2PPlug', 'Kalay Home',  \
			   'P2PCamLive', 'P2PCamCEO', 'Kalay Cam',  'VSaaS',   'DoorPhone',   \
			   'DVR/NVR',	'Kalay Car', 'Test Tools', 						  \
			   \
			   'IOTC Release Package', 'IOTC RC Package', 'IOTC New SOC Support', \
			   'IOTC Test Build', 'Partial Source Code', 'Kalay Box', 			  \
			   'UI Material', 'IOTC New SOC Customization', 'PCX Inside', 		  \
			   'Firmware', 'Alcatel', 'KPNS', 'MQTT SDK', 						  \
			   \
			   'P2P', 'Master', 'TPNS', 'Command Server', 'Watchdog', 'Athena',   \
			   'VSaaS', 'SPI']
	
	return catalog

def match_product_catalog(product_catalog):

	catalog_list = get_catalog()

	# return [str for str in catalog_list if str.lower() == product_catalog.lower()][0]
	for item in catalog_list:
		if item.lower() == product_catalog.lower():
			return item
	return None


########################################################################


def load_properties(file_path, sep='=', comment_char='#'):
	"""
	Read the file passed as parameter as a properties file.
	"""
	props = {}
	with open(file_path, "rt") as f:
		for line in f:
			l = line.strip()
			if l and not l.startswith(comment_char):
				key_value = l.split(sep)
				key = key_value[0].strip()
				value = sep.join(key_value[1:]).strip('" \t') 
				props[key] = value 
	return props

def export_properties(properties_paths):
	"""
	export environment variables from properties files
	"""

	if len(properties_paths) == 0:
		return

	paths = properties_paths.split(',')
	for path in paths:
		env_dict = load_properties(path)

		for key in sorted(env_dict.iterkeys()):
			os.environ[key] = env_dict[key]

def save_dict_to_json(dict, file_path):
	'''
	save keys and values of dictionary to json file
	'''
	with open(file_path, 'w') as fp:
		json.dump(dict, fp)


########################################################################


def get_artifact_file_path():
	'''
	artifact file path
	'''
	file_path = ''
	if is_valid_environ_key('OUTPUT_FILE_PATH'):
		file_path = os.environ['OUTPUT_FILE_PATH']
	elif is_valid_environ_key ('BUILD_OUTPUT_FILENAME'):
		file_path = os.environ['BUILD_OUTPUT_FILENAME']
	return file_path

def get_version_key(platform):
	"""
	version key for platform 
	"""
	version_key = ''
	if platform.lower() == 'sdk':
		version_key = 'sdk_version'
	elif platform.lower() == 'server':
		version_key = 'server_version'
	elif platform.lower() == 'android' or platform.lower() == 'ios':
		version_key = 'app_version'
	return version_key

def get_output_json_file_path(srvm_path, json_name):
	'''
	'''
	path_componenets = srvm_path.split('/')
	path_componenets.pop()
	path_componenets.append(json_name)
	path = '/'.join(path_componenets)
	return path

	
########################################################################


def is_valid_git_branch(git_branch):
	''' 
	supported git branches: master or release (release/*)
	'''
	is_valid_branch = ('master' not in git_branch and 'release' not in git_branch)
	
	if is_valid_branch and is_valid_build_environment('BUILD_CONFIGURATION'):
		print "[SRVM] Exits"
		print "[SRVM] Branch name: " + git_branch
		print "[SRVM] Build configuration: " + build_configuration
		return False
	else:
		return True

def is_valid_catalog(product_catalog):
	'''
	'''
	catalog_list = get_catalog()
	return any([str for str in catalog_list if str.lower() == product_catalog.lower()])

def is_valid_environ_key(key):
	if os.environ.has_key(key) and os.environ[key] != '':
		return True
	else:
		return False

def is_valid_build_environment(key):
	if is_valid_environ_key(key):
		print "[SRVM] found BUILD_CONFIGURATION: " + os.environ[key]

		global build_configuration
		build_configuration = os.environ[key]

	if build_configuration.lower() == 'Debug'.lower():
		print "[SRVM] BUILD_CONFIGURATION: Debug"
		return False
	else:
		print "[SRVM] BUILD_CONFIGURATION: Staging or Production"
		return True


########################################################################


def get_params(url_file):
	'''
	'''
	# required
	platform 		= os.environ['BUILD_PLATFORM']
	product_catalog = match_product_catalog(os.environ['SRVM_PRODUCT_CATALOG'])
	version_key 	= get_version_key(platform)

	params = {'release_for': 	 os.environ['SRVM_RELEASE_FOR'], \
			  'release_by':  	 os.environ['SRVM_RELEASE_BY'] + '@tutk.com', \
			  version_key:		 os.environ['BUILD_VERSION'], \
			  'product_catalog': product_catalog, \
			  'platform': 		 platform, \
			  'program_file': 	 url_file }

	# optional
	# client ID
	if is_valid_environ_key('SRVM_CUSTOMER_IDS'):
		params.update({'customer_ids': os.environ['SRVM_CUSTOMER_IDS']})

	# iOS only
	if os.environ['BUILD_PLATFORM'] == 'ios':
		params.update({'bundle-identifier': os.environ['BUILD_BUNDLE_ID']})
		params.update({'bundle-version': os.environ['BUILD_VERSION']})	# plist
	
	# SDK versions (for Apps only)
	if is_valid_environ_key('SDK_IOTC_VERSION'):
		params.update({'api_IOTC': os.environ['SDK_IOTC_VERSION']})
	if is_valid_environ_key('SDK_AV_VERSION'):
		params.update({'api_AV': os.environ['SDK_AV_VERSION']})
	if is_valid_environ_key('SDK_RDT_VERSION'):
		params.update({'api_RDT': os.environ['SDK_RDT_VERSION']})
	if is_valid_environ_key('SDK_TUNNEL_VERSION'):
		params.update({'api_Tunnel': os.environ['SDK_TUNNEL_VERSION']})

	if is_valid_environ_key('IS_FOR_GENERIC_VERSION'):
		params.update({'generic': os.environ['IS_FOR_GENERIC_VERSION']})

	# others
	if is_valid_environ_key('RD_NOTES'):
		params.update({'rd_notes': os.environ['RD_NOTES']})
	if is_valid_environ_key('BUILD_SUMMARY'):
		params.update({'summary': os.environ['BUILD_SUMMARY']})
	return params
	
def release_to_SRVM(url_file):
	""" 
	SRVM API, NOTE: bundle_version is the iOS app build version 
	"""
	params = get_params(url_file)

	# request
	srvm_url = host + 'ci/'
	r = requests.get(srvm_url, params=params)
	
	print "request: "  + r.url
	print "response: " + r.content
	
	return (r.content, params)

def parse_response(response):
	'''
	parse srvm response
	'''
	success = host in response
	return success

def update_json_dict(params, success, response):
	'''
	update json dictionary with addtional keys and values
	'''
	params.update({'success':       success})
	params.update({'success_title': "SRVM release"})
	params.update({'title_link':    ""})
	params.update({'error_msg':     ""})
	params.update({'git branch':    os.environ['GIT_BRANCH']})

	if success:
		url = 'https://' + response.split('://')[-1]
		params.update({'title_link': url})
		params.update({'SRVM URL': url})
	else:
		params.update({'error_msg': response})

	if is_valid_environ_key('BUILD_URL'):
		params.update({'Jenkins URL': os.environ['BUILD_URL']})

	return params


########################################################################


if __name__ == "__main__":

	# export environment variables from stdin properties files
	if len(sys.argv) > 1:
		properties_paths = sys.argv[1]
		export_properties(properties_paths)

	# check validations
	is_valid = True
	success  = False

	# supported git branches: master or release (release/*)
	if not is_valid_git_branch(os.environ['GIT_BRANCH']):
		print "[SRVM] Git branch: " + os.environ['GIT_BRANCH']
		is_valid = False
		success  = True
		
	file_path = get_artifact_file_path()
	if not file_path or len(file_path) == 0:
		print "[SRVM] Error: no valid output path found for OUTPUT_FILE_PATH or BUILD_OUTPUT_PATH and BUILD_OUTPUT_FILENAME"
		is_valid = False

	if not is_valid_catalog(os.environ['SRVM_PRODUCT_CATALOG']):
		print "[SRVM] Error: cannot find a matching value for input Product Catalog"
		is_valid = False

	if is_valid_environ_key('RELEASE_TO_SRVM'):
		print "[SRVM] Release to SRVM: " + os.environ['RELEASE_TO_SRVM']
		if os.environ['RELEASE_TO_SRVM'].lower() in ["true", "false"]:
			if os.environ['RELEASE_TO_SRVM'].lower()=="true":
				is_valid = True
			else:
				is_valid = False
		else:
			print "[SRVM] Warning: unknown value found for key, RELEASE_TO_SRVM"

	json_dict = {}

	if is_valid:
		url_file = os.environ['BUILD_URL'] + "/artifact/" + file_path
		(response, params) = release_to_SRVM(url_file)
		success  = parse_response(response)

		# dump json_dict to json file
		json_dict = update_json_dict(params, success, response)
	else:
		params    = get_params('')
		json_dict = update_json_dict(params, success, 'No SRVM release or srvm.py failed')

	json_path = get_output_json_file_path(sys.argv[0], "result.json")
	save_dict_to_json(json_dict, json_path)

	sys.exit(0)

