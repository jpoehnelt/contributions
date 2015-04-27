import requests
import json

JSON_HEADERS = {"Content-Type": "application/json"}

data = {
"id": 2123,
"owner": u"user",
"name": u"test_repo",
"project_number": 1
}
print(str(type(data['owner'])))
r = requests.post('http://contributions-907.appspot.com/api/project', data=json.dumps(data), headers=JSON_HEADERS)
print r.text
print str(r.status_code)