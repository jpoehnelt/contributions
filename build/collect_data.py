import requests
import json


PROJECTS_FILE = 'projects.json'
STUDENTS_FILE = 'students.json'
COMMITS_FILE = 'commits.json'

PROJECT_API_URL = 'http://contributions-907.appspot.com/api/project'
STUDENT_API_URL = 'http://contributions-907.appspot.com/api/student'
COMMIT_API_URL = 'http://contributions-907.appspot.com/api/commit'


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

'''
def get_repo(repo_name, project_number):
    print "Getting Repo: %s" % repo_name

    # Create project in database
    data = {
        "project_number": project_number,
        "repo_name": repo_name
    }

    response = requests.post(PROJECT_API_URL, data=json.dumps(data), auth=('cs399contributions', 'contributions399'))

    # error handling for posting project

    if response.status_code == 200:
        pass
    elif response.status_code == 409:
        # already exists
        response = requests.get(PROJECT_API_URL + "/%s" % repo_name, auth=('cs399contributions', 'contributions399'))
    else:
        raise Exception()

    project = response.json

    # get all of the commits and contributors from the commits
    parse_commits(project)

    print "Found %d Commits" % project['commit_count']

    print "Saving Number of Commits to Project"
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
    project['commit_count'] = 0
    print "Getting Commits for: %s" % project['repo_name']
    '''

#how many repos are we tracking per project?
for i, proj_number in enumerate(GITHUB_REPOS):
	print("Tracking "+str(len(proj_number))+ " Project#"+str(i)+" files")

def get_projects():
	"""
	Gets all of the project repos listed in GITHUB_REPOS and puts them into a projects list.
	Each element of the projects list represents one of the 5 projects. Each element is a list itself,
	with each element being one of the teams for the project. The element is a dict that has relevant
	info about each member.
	"""
	projects = []  # 0 will be all project 1 repos, etc

	for i, proj_number in enumerate(GITHUB_REPOS):
		projects.append([])  # create empty list to hold this project's repos
		#for each repo we have
		for project in proj_number:
			# create dict to hold all current project information that we gather
			temp_proj = {'url': 'http://www.github.com/' + project,
					 'owner': '',
					 'team_members': {},
					 'total_commits': 0}

			total_commits = 0
			print("Fetching commits for project: "+(''.join(project)))
			#get commit log
			next_url = 'https://api.github.com/repos/'+(''.join(project))+'/commits'
			while next_url:

				r = requests.get(next_url, auth=('cs399contributions', 'contributions399'))
				#convert JSON string into Python nested dictionary/list
				json_contrib = json.loads(r.text)

				for commit in json_contrib:
					total_commits += 1
					team_member = commit['commit']['author']['name']
					if team_member not in temp_proj['team_members']:  # check if member has been added
						temp_proj['team_members'][team_member] = {}   # add member
						team_member = temp_proj['team_members'][team_member] # team_member's actual name
						if not commit['author']:  # not a "contributor" so they don't have author info
							team_member['username'] = None
							team_member['email'] = None
							team_member['avatar_url'] = None 		  
						else: 		      # otherwise get their info
							team_member['username'] = commit['author']['login']
							team_member['email'] = commit['commit']['author']['email']
							team_member['avatar_url'] = commit['author']['avatar_url']
						
						team_member['commits'] = 1  # this is the first commit from them
					
					else:				# member already existed in team_members    
						temp_proj['team_members'][team_member]['commits'] += 1

				# api only gets 30 commits at a time, so need to get the next page link
				if 'next' in r.links:
					next_url = r.links['next']['url']
				else:
					next_url = ''

			print("Total commits: " + str(total_commits)) 
			temp_proj['total_commits'] = total_commits
			#print(temp_proj)
			projects[i].append(temp_proj) # add the current repo info to the projects list
	return projects

def write_to_file(data):
	"""
	Takes the projects list generated by get_projects() and prints it to a file.
	:param data: All of the project data that the get_projects() method returns
	"""
	f = open('collected_data.txt', 'w')
	for i, proj in enumerate(data):
		f.write("====================== Project %d ================================\n" % (i+1))
		f.write("\n")
		for repo in proj:
			f.write(str(repo))
			f.write(", \n")
	print("data written to file 'collected_data.txt'")
	f.close()



'''
    # TODO Parse commit
    # Add students found

    # Increment commit counter
    project['commit_count'] += 1


def save_commit(data):
    pass


if __name__ == "__main__":
    for i, project_list in enumerate(GITHUB_REPOS):
        # projects are not zero based
        project_number = i + 1

        print "*** Getting Repos for Project #%d ***" % project_number

        for project in project_list:
            get_repo(project, project_number)
'''