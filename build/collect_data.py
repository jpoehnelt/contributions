import gevent
from gevent.pool import Pool
import requests
import json
import time


PROJECTS_FILE = 'projects.json'
STUDENTS_FILE = 'students.json'
COMMITS_FILE = 'commits.json'

JSON_HEADERS = {'Content-Type': 'application/json'}
OUR_WEBSITE_URL = 'http://contributions-907.appspot.com/'
# OUR_WEBSITE_URL = 'http://localhost:8080/'

PROJECT_API_URL = OUR_WEBSITE_URL + 'api/project'
CONTRIBUTOR_API_URL = OUR_WEBSITE_URL + 'api/contributor'
COMMIT_API_URL = OUR_WEBSITE_URL + 'api/commit'

ALLOWED_FIELDS_FOR_FILES = ['filename', 'sha', 'additions', 'deletions', 'changes', 'contents_url',
                            'raw_url', 'blob_url']

ALL_REPOS_COMMITS_URLS = []

AUTH = ('cs399contributions', 'contributions399')

GITHUB_REPOS = [
    # band
    ['Adam-Thomas/Band-Proj1', 'alecdavidson/joyful-waves', 'AustinAbhari/CS399_TheBand',
     'c1phr/cs399_band', 'cmh553/theBand', 'DylanGrayson/CS399_TheBand', 'itj3/bandPage',
     'justinwp/cs399-band', 'kbullins/CS399Band', 'lf237/band', 'lmk243/BandProject',
     'sk367/cs399_band'],
    # theatre
    ['sk367/cs399_Theater', 'Adam-Thomas/Theatre-Proj2', 'brandonparee/theTheatre',
     'c1phr/cs399_theatre', 'dukeayers/cs399_theater', 'FlintyFalcon/Project2',
     'kyleamcginn88/Theatre', 'lf237/theatre', 'mkgilbert/cs399_the_theatre',
     'yourbuddyconner/cs399-theatre'],
    #agency
    ['alexlanza/cs399_agency', 'brandonparee/theAgency', 'dukeayers/cs399_agency',
     'DylanGrayson/Agency_Proj3', 'lf237/agency', 'kyleamcginn88/Agency', 'vtsyms/CS399Agency',
     'yourbuddyconner/cs399-agency'],
    #social
    ['cmh553/cs399_social', 'coop741/CS399Social', 'c1phr/cs399_social',
     'DylanGrayson/social_proj4', 'dukeayers/cs399_SocialMedia', 'ErinBailey/cs399-social',
     'yourbuddyconner/cs399-social'],
    #final
    ['breadraptor/cs399_final', 'cap377/cs399final', 'EduardoIniguez/CS399-final',
     'justinwp/contributions', 'alexlanza/CS399-Final', 'DylanGrayson/knobsock', 'lf237/project5',
     'c1phr/cs399_final']
]
DUE_DATE_MAPPING = ["2015-01-23", "2015-02-06", "2015-02-20", "2015-04-03"]

collected_contributors = {}  # stores all the non-github-user's 'collected_contributors' so we don't add more than one
commits = []
pool = Pool(30)

RETRIES = 5

def get_current_commits():
    print 'Getting current commits... this may take awhile'
    for commit in json.loads(get_url(COMMIT_API_URL, timeout=60).text)['objects']:
        commits.append(commit['id'])

    print commits

def get_url(url, auth=None, timeout=4):
    """
    Requests does not make more than a single get attempt.
    :param url: url to get
    :param auth: tuple for basic auth
    :return: response
    """
    tries = 1
    while tries < RETRIES:
        try:
            print "Getting: %s Try: %d" % (url, tries)
            return requests.get(url, auth=AUTH, timeout=timeout)
        except requests.ConnectionError as e:
            print e
            tries += 1
            time.sleep(tries**2)
            continue
        except Exception as e:
            print e

    raise requests.ConnectionError()



def get_repo(repo_name, project_number):
    response = get_url('https://api.github.com/repos/' + repo_name, AUTH)
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

    # get all commits from github
    get_repo_commits(data, repo_json_data['full_name'])


def get_id(name):
    """
    Some contributors on github don't have logins. This means they don't have an ID on github.
    Since we are having to manually put ID's into datastore using the API, we need to have a number
    to use as the contributor's ID. I am generating a random number that is bigger than the current
    github user ID numbers, so hopefully we won't ever accidentally generate an existing ID.
    """

    return sum([ord(c) * 2 ** i for i, c in enumerate(name)])


def save_repo(data, full_repo_name):
    # add the repo to the datastore
    response = requests.post(PROJECT_API_URL, data=json.dumps(data), headers=JSON_HEADERS)

    # error handling for posting project
    if response.status_code == 201:
        print("Added repo %s to datastore" % full_repo_name)

        # wait one second to give the datastore time to catch up (commits rely on this being in there)
        time.sleep(0.5)

    elif response.status_code == 409:
        print("Repo already exists. Getting repo %s." % full_repo_name )

    else:
        raise Exception("The response was " + str(response.status_code))


def get_repo_commits(project, repo_name):
    """
    Gets all commits for the repo
    :param project: the data dictionary with project details
    :param repo_name: full name of repo like <username>/cs399_the_theatre
    :param repo_id: github's id of the repo
    :return: None
    """
    url = 'https://api.github.com/repos/' + (''.join(repo_name)) + '/commits'
    while url:
        print "==========================="
        print 'Getting commits: %s' % url
        r = get_url(url, AUTH)

        print "Current rate limit remaining %s." %r.headers['x-ratelimit-remaining']

        #convert JSON string into Python nested dictionary/list
        json_commits = json.loads(r.text)

        # for commit in json_commits:
        #     # send data to be processed and saved to datastore
        #     print "---------------------------"
        #     parse_single_commit(commit['url'], project['id'])
        #     time.sleep(0.1) # keep from hitting rate limit on github

        pool.map(parse_single_commit, [[commit['url'], project['id']] for commit in json_commits])

        # api only gets 30 commits at a time, so need to get the next page link
        if 'next' in r.links:
            url = r.links['next']['url']
        else:
            break

    return


def save_contributor(data):
    print "Contributor username: %s" % data['username']
    if data['username'] in collected_contributors:  # we don't want to create more of the same contributor
        print("Contributor %s has already been added." % data['username'])
        return

    # post new contributor
    response = requests.post(CONTRIBUTOR_API_URL, data=json.dumps(data), headers=JSON_HEADERS)

    if response.status_code == 201:
        print("Added contributor " + data['username'] + " to datastore.")
        collected_contributors[data['username']] = data
    elif response.status_code == 409:
        print("Contributor " + data['username'] + " is a duplicate entity.")
        collected_contributors[data['username']] = data
    else:
        raise Exception("The response was %d " % response.status_code)


def parse_single_commit(args):
    """
    :param data: repo_name, username, github api url that holds the commit data
    """

    url = args[0]
    project_id = args[1]
    sha = url.split('/')[-1]
    if sha in commits:
        print "Already have commit: %s" % sha
        return

    print "Parsing Commit: %s" % url
    r = get_url(url, auth=AUTH)
    commit_json_data = json.loads(r.text)
    contributor = {
        'id': None,
        'name': None,
        'username': None,
        'email': None,
    }

    # get contributor's info
    if not commit_json_data['author']:
        # not a listed github user so they don't have author info
        print("No author for commit")

        # first set their name and username to be the same for now
        contributor['name'] = commit_json_data['commit']['author']['name']
        contributor['username'] = contributor['name']
        if contributor['username'].lower() != 'unknown':
            print("Searching GitHub for %s " % contributor['username'])

            # see if we can find the user on github to get their info...
            response = get_url('https://api.github.com/users/%s' % contributor['username'],
                                    auth=AUTH)

            if response.status_code == 200:
                # they are a github user, so use this info
                print("User found %s " % contributor['username'])

                # load response
                user_data = json.loads(response.text)
                contributor['username'] = user_data['login']
                contributor['id'] = user_data['id']

                # some fields are optional
                if 'email' in user_data:
                    contributor['email'] = user_data['email']

                if 'avatar_url' in user_data:
                    contributor['avatar_url'] = user_data['avatar_url']

                if 'name' in user_data:
                    contributor['name'] = user_data['name']

            else:
                print("User not found %s " % contributor['username'])

                # use hash function on name to get consistent id
                contributor['id'] = get_id(contributor['username'])
        else:
            # unknown username
            contributor['id'] = get_id(contributor['username'])


    else:  # they are a listed github user so get their info from the commit
        contributor['id'] = commit_json_data['author']['id']
        contributor['name'] = commit_json_data['commit']['author']['name']
        contributor['username'] = commit_json_data['author']['login']
        contributor['email'] = commit_json_data['commit']['author']['email']
        contributor['avatar_url'] = commit_json_data['author']['avatar_url']

    # add contributor to datastore
    save_contributor(contributor)

    files = []
    # remove all fields not in file model. for example previous_file
    for commit_file in commit_json_data['files']:
        single_file = {}
        for field, value in commit_file.iteritems():
            if field in ALLOWED_FIELDS_FOR_FILES:
                single_file[field] = value
        files.append(single_file)

    commit_data = {
        'id': commit_json_data['sha'],
        'contributor': contributor['id'],
        'project': project_id,
        'date': commit_json_data['commit']['author']['date'],
        'message': commit_json_data['commit']['message'][:499],
        'changes': commit_json_data['stats']['total'],
        'additions': commit_json_data['stats']['additions'],
        'deletions': commit_json_data['stats']['deletions'],
        'files': files
    }


    save_commit(commit_data)


def save_commit(data):

    response = requests.post(COMMIT_API_URL, data=json.dumps(data), headers=JSON_HEADERS)

    # error handling for posting commit
    if response.status_code == 201:
        print("Added commit %s to datastore." % data['id'])
    elif response.status_code == 409:
        print("Commit %s already exists. Continuing... " % data['id'])
    else:
        print "Could not add commit %s" % data['id']


if __name__ == "__main__":
    get_current_commits()
    for i, project_list in enumerate(GITHUB_REPOS):
        # projects are not zero based
        project_number = i + 1

        for project in project_list:
            get_repo(project, project_number)

