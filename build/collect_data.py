import requests
import json
import random
import time


PROJECTS_FILE = 'projects.json'
STUDENTS_FILE = 'students.json'
COMMITS_FILE = 'commits.json'

JSON_HEADERS = {'Content-Type': 'application/json'}
OUR_WEBSITE_URL = 'http://contributions-907.appspot.com/'
#OUR_WEBSITE_URL = 'http://localhost:9080/'

PROJECT_API_URL = OUR_WEBSITE_URL + 'api/project'
STUDENT_API_URL = OUR_WEBSITE_URL + 'api/contributor'
COMMIT_API_URL = OUR_WEBSITE_URL + 'api/commit'

ALL_REPOS_COMMITS_URLS = []
GITHUB_REPOS = [
    #band
    ['Adam-Thomas/Band-Proj1', 'alecdavidson/joyful-waves','AustinAbhari/CS399_TheBand','c1phr/cs399_band','cmh553/theBand','DylanGrayson/CS399_TheBand','itj3/bandPage','justinwp/cs399-band','kbullins/CS399Band','lf237/band','lmk243/BandProject','sk367/cs399_band'],
    #theatre
    ['sk367/cs399_Theater', 'Adam-Thomas/Theatre-Proj2','brandonparee/theTheatre','c1phr/cs399_theatre','dukeayers/cs399_theater','FlintyFalcon/Project2','kyleamcginn88/Theatre','lf237/theatre','mkgilbert/cs399_the_theatre', 'yourbuddyconner/cs399-theatre'],
    #agency
    ['alexlanza/cs399_agency','brandonparee/theAgency','dukeayers/cs399_agency','DylanGrayson/Agency_Proj3','lf237/agency','kyleamcginn88/Agency','vtsyms/CS399Agency','yourbuddyconner/cs399-agency'],
    #social
    ['cmh553/cs399_social','coop741/CS399Social','c1phr/cs399_social','DylanGrayson/social_proj4','dukeayers/cs399_SocialMedia','ErinBailey/cs399-social','yourbuddyconner/cs399-social'],
    #final
    ['breadraptor/cs399_final','cap377/cs399final','EduardoIniguez/CS399-final']
]
DUE_DATE_MAPPING = ["2015-01-23", "2015-02-06", "2015-02-20", "2015-04-03"]

##### TESTING - just grap one project ######
#GITHUB_REPOS = [['sk367/cs399_Theater']]

usernames = {} # stores all the non-github-user's 'usernames' so we don't add more than one

def get_repo(repo_name, project_number):
    print "Getting Repo: %s" % repo_name

    # get repo info
    response = requests.get('https://api.github.com/repos/' + repo_name, auth=('cs399contributions', 'contributions399'))
    repo_json_data = json.loads(response.text)

    # Create project in database
    data = {
    	"id": repo_json_data['id'],
        "project_number": project_number,
        "name": repo_json_data['name'],
        "owner": repo_json_data['owner']['login']
    }
    

    # save repo into the datastore
    save_repo(data, repo_json_data['full_name'])

    # get all commits from github, store them, and get the total count
    commit_count = parse_commits(data, repo_json_data['full_name'], repo_json_data['id'])
    data['commit_count'] = commit_count
    print "Saving %d Commits to Project" % data['commit_count']
    
    # this is where we would update the projects with the commit_count, but "put" doesn't work yet

	### For testing the 'Put' method. Currently does NOT work ###
    # update = {
    #     "project_number": project_number,
    #     "repo_name": repo_name
    # }

    #response = requests.put(PROJECT_API_URL + "/%d" % repo_json_data['id'], data=json.dumps(update),
    #						headers=JSON_HEADERS)

def generate_random_id():
	"""
	Some contributors on github don't have logins. This means they don't have an ID on github.
	Since we are having to manually put ID's into datastore using the API, we need to have a number
	to use as the contributor's ID. I am generating a random number that is bigger than the current
	github user ID numbers, so hopefully we won't ever accidentally generate an existing ID.
	"""
	random.seed()
	id = random.randint(100000000, 999999999)
	return id


def save_repo(data, full_repo_name):
    # add the repo to the datastore
    response = requests.post(PROJECT_API_URL, data=json.dumps(data), headers=JSON_HEADERS)

    # error handling for posting project
    if response.status_code == 201:
    	# successfully created
    	print("")
    	print("////////////////////////////////////////////////////////////////////////")
    	print("**** added repo " + full_repo_name + " to datastore ****")
    	print("waiting one second...")
    	print("////////////////////////////////////////////////////////////////////////")
    	print("")
    	# wait one second to give the datastore time to catch up (commits rely on this being in there)
    	time.sleep(1)

    elif response.status_code == 409:
        # already exists
        print("**** repo already existed. Getting repo " + full_repo_name + "****")
        response = requests.get(PROJECT_API_URL + "/%d" % data['id'], headers=JSON_HEADERS)
    
    else:
        raise Exception("The response was " + str(response.status_code))


def parse_commits(project, repo_name, repo_id):
	"""
	Gets all commits for the repo
	:param project: the data dictionary with project details
	:param repo_name: full name of repo like <username>/cs399_the_theatre
	:param repo_id: github's id of the repo 
	:return: None
	"""
	print("")
	print("########################################################################")
	print "**** Getting Commits for: %s" % repo_name + " ****"
	print("########################################################################")	
	print("")

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
				# first set their name and username to be the same for now
				contrib_info['name'] = commit['commit']['author']['name']
				contrib_info['username'] = contrib_info['name']
				# see if we can find the user on github to get their info...
				
				response = requests.get('https://api.github.com/users/' + contrib_info['username'], auth=('cs399contributions', 'contributions399'))
				print("")
				print("------- User info not available in commit. Checking GitHub for user " + contrib_info['username'] + "-------")
				print("")
				if response.status_code == 200 and contrib_info['username'].lower() != 'unknown': # they are a github user, so use this info
					print("user found!")
					user_data = json.loads(response.text)
					contrib_info['username'] = user_data['login']
					contrib_info['id'] = user_data['id']
					if 'email' not in user_data: # this was a fun one. Some user accounts don't have an email...Why Github??
						contrib_info['email'] = None
					else:
						contrib_info['email'] = user_data['email']
					if 'avatar_url' not in user_data:
						contrib_info['avatar_url'] = None
					else:
						contrib_info['avatar_url'] = user_data['avatar_url']
					if 'name' not in user_data:
						contrib_info['name'] = None
					else:
						contrib_info['name'] = user_data['name']

				else: # the username didn't exist on github
					# so we need to generate an id
					print("user not found :(")
					if  contrib_info['username'] not in usernames:
						contrib_info['id'] = generate_random_id()
					else:
						contrib_info['id'] = usernames[contrib_info['username']]
					contrib_info['email'] = None
					contrib_info['avatar_url'] = None 
		  
			else: 	# they are a listed github user so get their info from the commit
				contrib_info['id'] = commit['author']['id']
				contrib_info['name'] = commit['commit']['author']['name']
				contrib_info['username'] = commit['author']['login']
				contrib_info['email'] = commit['commit']['author']['email']
				contrib_info['avatar_url'] = commit['author']['avatar_url']

			# add contributor to datastore
			add_contrib(contrib_info)
   
			# store the information for the commit
			commit_info = {}  # the commit's project repo_name, user_id, and commit url
			
			commit_info['user_id'] = contrib_info['id']	
			commit_info['username'] = contrib_info['username']			
			# store commit project repo_name
			commit_info['repo_id'] = repo_id
			# store commit api url
			commit_info['commit_api_url'] = commit['url']
			
			# send data to be processed and saved to datastore
			save_commit(commit_info)

		# api only gets 30 commits at a time, so need to get the next page link
		if 'next' in r.links:
			next_url = r.links['next']['url']

		else:
			next_url = ''
	return project['commit_count']


def add_contrib(data):

	if data['username'] not in usernames:  # we don't want to create more of the same contributor
		usernames[ data['username'] ] = int(data['id'])

		response = requests.post(STUDENT_API_URL, data=json.dumps(data), headers=JSON_HEADERS)

		if response.status_code == 201:
			print("")
			print("*** Added contributor " + data['username'] + " to datastore ***")
			# wait one second to give the datastore time to catch up (commits rely on the contrib)
			print("waiting one second...")
			print("")
			time.sleep(1)
    		
		elif response.status_code == 409:
			# already exists
			print("*** Contributor " + data['username'] + " already exists ***")
			
		else:
			raise Exception("The response was " + str(response.status_code))
	else:
		print("=== Contributor " + data['username'] + " already exists ===")


def _get_commit_info(data):
	"""
	:param data: repo_name, username, github api url that holds the commit data
	"""
	r = requests.get(data['commit_api_url'], auth=('cs399contributions', 'contributions399'))
	commit_json_data = json.loads(r.text)

	# convert commit's hex code to integer so we can store it in the datastore
	commit_id = int(commit_json_data['sha'], 16) # type longInt ! Won't store in db
	commit_id = int(commit_id % 100000000) # shortens and converts to regular int

	contributor = data['user_id']
	project = data['repo_id']
	date = commit_json_data['commit']['author']['date']
	message = commit_json_data['commit']['message'][:499] # ndb can't store more than 500 chars...

	changes = commit_json_data['stats']['total']
	additions = commit_json_data['stats']['additions']
	deletions = commit_json_data['stats']['deletions']

	# # some commits don't have stats
	# if 'stats' not in commit_json_data:
	# 	changes = 0
	# 	additions = 0
	# 	deletions = 0
	# else:
	# 	changes = commit_json_data['stats']['total']
	# 	additions = commit_json_data['stats']['additions']
	# 	deletions = commit_json_data['stats']['deletions']

	commit_data = {
					'id': commit_id,
					'contributor': contributor,
					'project': project,
					'date': date,
					'message': message,
					'changes': changes,
					'additions': additions,
					'deletions': deletions,
	}
	
	return commit_data


def save_commit(data):
	"""
	Saves the commit to the datastore
	:param data: should be in format {'repo_id': '', 'user_id': '', 'commit_api_url': ''}
	"""
	# get detailed commit information in python dict form	
	print("*** Getting commit info for " + data['username'] + " ***")
	commit_data = _get_commit_info(data)
	print("")
	print("********************************************************************")
	print(" Commit data ")
	print("********************************************************************")
	print(commit_data)

	response = requests.post(COMMIT_API_URL, data=json.dumps(commit_data), headers=JSON_HEADERS)

    # error handling for posting project
	if response.status_code == 201:
	# successfully created
	    print("*** Added commit by contributor " + data['username'] + " to datastore ***")
	elif response.status_code == 409:
	    # already exists
	    print("Commit " + str(commit_data['id']) + " already existed. Continuing... ")
	else:
		raise Exception("The response was " + str(response.status_code))


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
		print("")
		print("")
		print("...............................................................................")
		print("")
		print("               *** Getting Repos for Project #%d ***" % project_number)
		print("")
		print("...............................................................................")
		print("")
		print("")
		for project in project_list:
			get_repo(project, project_number)

		print("")
		print("************** COMPLETE *****************")

