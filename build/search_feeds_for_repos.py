import requests
import feedparser
import json
import pprint
AUTH = ('cs399contributions', 'contributions399')
EXCLUDE = ['cs413', 'cs480', 'cs386', 'capstone', 'cs345', 'daemon']


def get_projects():
    r = requests.get('http://contributions-907.appspot.com/api/project')

    if r.status_code != 200:
        raise Exception

    return ["/".join([p['owner'], p['name']]).lower() for p in json.loads(r.text)['objects']]

def get_contributors():
    """
    Gets contributors from our api
    :return: list of contributors
    """
    r = requests.get('http://contributions-907.appspot.com/api/contributor')

    if r.status_code != 200:
        raise Exception

    # get only valid github users
    return [c['username'] for c in json.loads(r.text)['objects']
            if c['avatar_url'] is not None and 'gitter' not in c['username']]

def get_atom_feed(user):
    """
    Gets the users' atom feed
    :param user: github user
    :return: feed
    """
    r = requests.get('https://github.com/%s.atom' % user, auth=AUTH)

    if r.status_code != 200:
        raise Exception

    return feedparser.parse(r.text)

if __name__ == "__main__":
    repos = {}

    projects = get_projects()

    for user in get_contributors():
        for entry in get_atom_feed(user).entries:
            if 'push' not in entry.title:
                continue

            repo = "/".join(entry['link'].split('/compare')[0].split('/')[-2:])

            if any([x.lower() in repo.lower() for x in EXCLUDE]):
                continue

            if repo.lower() in projects:
                continue

            if repo not in repos:
                repos[repo] = []

            if user not in repos[repo]:
                repos[repo].append(user)

    # remove repos where no other users are part of
    repos = { key:value for key, value in repos.items() if len(value) > 1}
    pprint.pprint(repos)

    with open('possible_repos.json', 'w') as f:
        f.write(json.dumps(repos, indent=4))