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
    ['Adam-Thomas/Band-Proj1','alecdavidson/joyful-waves','AustinAbhari/CS399_TheBand','c1phr/cs399_band','cmh553/theBand','DylanGrayson/CS399_TheBand','itj3/bandPage','justinwp/cs399-band','kbullins/CS399Band','lf237/band','lmk243/BandProject','sk367/cs399_band','smashfligaeta/CS399_TheBand'],
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

#Fetch commits
for i, proj_number in enumerate(GITHUB_REPOS):
    print("Tracking "+str(len(proj_number))+ " Project#"+str(i)+" files")
    i += 1

for proj_number in GITHUB_REPOS:
    for project in proj_number:
        print("Fetching commits for project: "+(''.join(project)))
        r = requests.get('https://api.github.com/repos/'+(''.join(project))+'/commits', auth=('cs399contributions', 'contributions399'))
        json_contrib = json.loads(r.text)
        print(json_contrib)


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