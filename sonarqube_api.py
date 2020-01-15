import requests
import json
import os

class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)

DEFAULT_HOST = 'http://localhost'
DEFAULT_PORT = '9000'
DEFAULT_BASE_PATH = ''

def create_profile(profile_name,language):
	#language = 'java'
	url = DEFAULT_HOST + ':' + DEFAULT_PORT+ '/api/qualityprofiles/create'
	data  = {'language':language, 'name':profile_name}
	response = requests.post(url, data=data, auth=('admin', 'admin'))

	##resp = requests.get('http://localhost:9000/api/qualitygates/list')
	if response.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('POST /api/qualityprofiles/create/ {}'.format(response.status_code))
	print('Created Profile. ID: {}'.format(response.json()["profile"]["key"]))
	return response
def copy_profile(profile_id, profile_name):
	#language = 'java'
	url = DEFAULT_HOST + ':' + DEFAULT_PORT+ '/api/qualityprofiles/copy'
	data  = {'fromKey':profile_id,'toName':profile_name}
	response = requests.post(url, data=data, auth=('admin', 'admin'))

	if response.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('POST /api/qualityprofiles/copy {}'.format(response.status_code))
	print('Copied Profile from : {} to {}'.format(profile_id,response.json()["name"]))
	return response

def create_quality_profile(profile_name):
	url = DEFAULT_HOST + ':' + DEFAULT_PORT+ '/api/qualitygates/create'
	data  = {'name':profile_name}
	response = requests.post(url, data=data, auth=('admin', 'admin'))
	print(response.json())
	if response.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('POST /api/qualitygates/create/ {}'.format(response.status_code))
	print('Created Quality Profile. ID: {}'.format(response.json()["id"]))
	return response
def copy_quality_profile(profile_id, profile_name):
	url = DEFAULT_HOST + ':' + DEFAULT_PORT+ '/api/qualitygates/copy'
	data  = {'id':profile_id,'name':profile_name}
	response = requests.post(url, data=data, auth=('admin', 'admin'))

	if response.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('POST /api/qualitygates/copy {}'.format(response.status_code))
	print('Copied Profile. ID: {}'.format(response.json()["id"]))
def create_group(groupname):
	url = DEFAULT_HOST + ':' + DEFAULT_PORT+ '/api/user_groups/create'
	data  = { 'name': groupname}
	response = requests.post(url, data=data, auth=('admin', 'admin'))
	if response.status_code != 200:
	    # This means something went wrong.
	    raise ApiError('POST /api/user_groups/create {}'.format(response.status_code))
	print('Created Group. ID: {}'.format(response.json()["group"]["id"]))
	return response
def add_user(username, group_id):
	url = DEFAULT_HOST + ':' + DEFAULT_PORT+ '/api/user_groups/add_user'
	data  = { 'id': group_id, 'login': username}
	print("calling add user with parameters " + str(data))
	response = requests.post(url, data=data, auth=('admin', 'admin'))
	if response.status_code != 204:
	    # This means something went wrong.
	    raise ApiError('POST /api/user_groups/add_user {}'.format(response.status_code))
	print('Added User {} to Group {}'.format(user_name, group_id ))
	return response

scenario_choice = os.getenv("scenario_choice")
profile_name = os.getenv("profile_name")
profile_language = os.getenv("profile_language")
group_name = os.getenv("group_name")
user_name = os.getenv("user_name")
copy_profile_id = os.getenv("copy_profile_id")
quality_copy_profile_id = os.getenv("quality_copy_profile_id")
quality_profile_name = os.getenv("quality_profile_name")


if scenario_choice == 'Create Profile':
	profile_details = create_profile(profile_name,profile_language)
	print("Profile created with details " + str(profile_details.json()))
elif scenario_choice == 'Copy Profile':
	profile_details = copy_profile(copy_profile_id,profile_name)
	print("Profile created with details " + str(profile_details.json()))
elif scenario_choice == 'Create Qualitygates Profile':
	profile_details = create_quality_profile(quality_profile_name)
	print("Quality Profile created with details " + str(profile_details.json()))
elif scenario_choice == 'Copy Qualitygates Profile':
	profile_details = copy_quality_profile(quality_copy_profile_id,quality_profile_name)
	print("Profile created with details " + str(profile_details.json()))
elif scenario_choice == 'Create Profile and Create Group':
	profile_details = create_profile(profile_name,profile_language)
	print("Profile created with details " + str(profile_details.json()))
	group_details = create_group(group_name)
	print("Group created with details " + str(group_details))
elif scenario_choice == 'Create Profile, Create Group and Add user into Group':
	profile_details = create_profile(profile_name,profile_language)
	print("Profile created with details " + str(profile_details.json()))
	group_details = create_group(group_name)
	print("Group created with details " + str(group_details.json()))
	user_details = add_user(user_name,group_details.json()["group"]["id"])
	print("Added user with details " + str(user_details))

else:
	raise ApiError('Invalid Input')

