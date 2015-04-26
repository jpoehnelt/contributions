import requests
import json


PROJECTS_FILE = 'projects.json'
STUDENTS_FILE = 'students.json'
COMMITS_FILE = 'commits.json'

PROJECT_API_URL = 'http://contributions-907.appspot.com/api/project'
STUDENT_API_URL = 'http://contributions-907.appspot.com/api/student'
COMMIT_API_URL = 'http://contributions-907.appspot.com/api/commit'

ALL_REPOS_COMMITS_URLS = []
GITHUB_REPOS = [
    #band
    ['Adam-Thomas/Band-Proj1','alecdavidson/joyful-waves','AustinAbhari/CS399_TheBand','c1phr/cs399_band','cmh553/theBand','DylanGrayson/CS399_TheBand','itj3/bandPage','justinwp/cs399-band','kbullins/CS399Band','lf237/band','lmk243/BandProject','sk367/cs399_band'],
    #theatre
    ['Adam-Thomas/Theatre-Proj2','brandonparee/theTheatre','c1phr/cs399_theatre','dukeayers/cs399_theater','FlintyFalcon/Project2','kyleamcginn88/Theatre','lf237/theatre','mkgilbert/cs399_the_theatre','sk367/cs399_Theater','yourbuddyconner/cs399-theatre'],
    #agency
    ['alexlanza/cs399_agency','brandonparee/theAgency','dukeayers/cs399_agency','DylanGrayson/Agency_Proj3','lf237/agency','kyleamcginn88/Agency','vtsyms/CS399Agency','yourbuddyconner/cs399-agency'],
    #social
    ['cmh553/cs399_social','coop741/CS399Social','c1phr/cs399_social','DylanGrayson/social_proj4','dukeayers/cs399_SocialMedia','ErinBailey/cs399-social','yourbuddyconner/cs399-social'],
    #final
    ['breadraptor/cs399_final','cap377/cs399final','EduardoIniguez/CS399-final']
]
DUE_DATE_MAPPING = ["2015-01-23", "2015-02-06", "2015-02-20", "2015-04-03"]

##### TESTING - just grap one project ######
#GITHUB_REPOS = [['EduardoIniguez/CS399-final']]

def get_repo(repo_name, project_number):
    print "Getting Repo: %s" % repo_name

    # Create project in database
    data = {
        "project_number": project_number,
        "repo_name": repo_name
    }

    response = requests.post(PROJECT_API_URL, data=json.dumps(data), auth=('cs399contributions', 'contributions399'))

    # error handling for posting project

    if response.status_code == 200 or response.status_code == 500:
        pass
    elif response.status_code == 409:
        # already exists
        response = requests.get(PROJECT_API_URL + "/%s" % repo_name, auth=('cs399contributions', 'contributions399'))
    else:
        raise Exception()
	
	#################################################################
	# TODO actually put the project information in the datastore
	#################################################################
	# now get the object we just posted
    #response = requests.get(PROJECT_API_URL + "/%s" % repo_name, auth=('cs399contributions', 'contributions399'))
	#project = json.loads(response.text)
	
	
	# get all of the commits and contributors from the commits
    total_commits = parse_commits(data)

    print "'Fake' Saving %d Commits to Project" % total_commits 
    update = {
        "project_number": project_number,
        "repo_name": repo_name
    }

    # response = requests.put(PROJECT_API_URL + "/%s" % repo_name, data=json.dumps(update))


def save_repo(data):
    pass


def parse_commits(project):
	"""
	Gets all commits for the repo
	:param project:
	:return: None
	"""
	repo_name = project['repo_name']

	print "Getting Commits for: %s" % repo_name
	
	project['commit_count'] = 0

	next_url = 'https://api.github.com/repos/'+(''.join(repo_name))+'/commits'
	while next_url:
		r = requests.get(next_url, auth=('cs399contributions', 'contributions399'))
		#convert JSON string into Python nested dictionary/list
		json_commits = json.loads(r.text)

		for commit in json_commits:
			project['commit_count'] += 1
			contrib_info = {} # used for adding a new contributor with add_contrib() method

			# get contributor's info 
			if not commit['author']:  # not a listed github user so they don't have author info
				contrib_info['name'] = commit['commit']['author']['name']
				contrib_info['username'] = contrib_info['name']
				contrib_info['email'] = None
				contrib_info['avatar_url'] = None 
		  
			else: 	# they are a listed github user so get their info
				contrib_info['name'] = commit['commit']['author']['name']
				contrib_info['username'] = commit['author']['login']
				contrib_info['email'] = commit['commit']['author']['email']
				contrib_info['avatar_url'] = commit['author']['avatar_url']

			###################################################################
			# TODO add contributor to datastore with add_contrib() method
			###################################################################
			#add_contrib(contrib_info)
	
			# store the information for the commit
			commit_info = {}  # the commit's project repo_name, username, and commit url
			
			# store contrib username
			if not contrib_info['username']:  # contrib. didn't have a username, only a name
				commit_info['username'] = contrib_info['name']
			
			else:  # contrib had a username
				commit_info['username'] = contrib_info['username']
								
			# store commit project repo_name
			commit_info['repo_name'] = repo_name
			# store commit api url
			commit_info['commit_api_url'] = commit['commit']['url']
			
			# send data to be processed and saved to datastore
			save_commit(commit_info)

		# api only gets 30 commits at a time, so need to get the next page link
		if 'next' in r.links:
			next_url = r.links['next']['url']

		else:
			next_url = ''
	return project['commit_count']

def add_contrib(data):
	##########################################################
	# TODO put student in datastore based on "data" dictionary
	##########################################################
	pass


def get_commit_info(commit_url):
	"""
	:param commit_url: api url that holds the commit data
	"""
	r = requests.get(commit_url, auth=('cs399contributions', 'contributions399'))
	commit_json_data = json.loads(r.text)
	return commit_json_data


def save_commit(data):
	"""
	data should be in format {'repo_name': '', 'username': '', 'commit_api_url': ''}
	"""
	###########################################################
	# TODO actually save the commit to the datastore
	###########################################################

	# get detailed commit information in python dict form	
	#commit_data = get_commit_info(data['commit_api_url'])
	# just save this to global variable for now to test it
	ALL_REPOS_COMMITS_URLS.append(data)
	print("Added commit for project " + data['repo_name'] + " made by " + data['username'])
	
	# TODO save the new commit to the datastore    
	return True


def write_to_file(data, filename):
	f = open(filename, 'w')
	for i, proj in enumerate(data):
		for repo in proj:
			f.write(str(repo))
			f.write(", \n")
	print("data written to file 'collected_data.txt'")
	f.close()


if __name__ == "__main__":
	for i, project_list in enumerate(GITHUB_REPOS):
		print("Tracking " + str(len(project_list)) + " Project#" + str(i) + " files")

		# projects are not zero based
		project_number = i + 1
		
		print("*** Getting Repos for Project #%d ***" % project_number)

		for project in project_list:
			get_repo(project, project_number)

