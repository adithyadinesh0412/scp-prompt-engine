import requests, json, os
# Construct the path to the JSON file
current_directory = os.path.dirname(__file__)  # Get the directory of the current script
project_json_file_path = os.path.join(current_directory, 'resource-descriptions', 'project.json')  # Construct the path
response_file = os.path.join(current_directory, 'api_response.txt')  # Construct the path

access_token = ""
host = "https://scp-qa.elevate-apis.shikshalokam.org"

def read_entity_types():
    url = str(host) +"/scp/v1/entity-types/read"

    payload = json.dumps({
    "value": [
        "categories",
        "recommended_for",
        "languages",
        "licenses",
        "duration"
    ]
    })
    access_token = login()
    headers = {
    'content-type': 'application/json',
    'x-auth-token': 'bearer ' + access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    entity_entityType_obj = {}

    try:
        if response.status_code == 200:
            response_data = response.json()
            for entity_types in response_data['result']['entity_types']:
                entity_entityType_obj[entity_types['value']] = []
                for entities in entity_types['entities']:
                    entity_entityType_obj[entity_types['value']].append(entities['value'])
    except ValueError as e:
        print("Invalid JSON response", e)
    
    return entity_entityType_obj

def login():
    url = str(host) +"/user/v1/account/login"
    payload = 'email=ccthree%40yopmail.com&password=Password%40123'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        if response.status_code == 200:
            response_data = response.json()
            return response_data['result']['access_token']
            
    except ValueError as e:
        print("Invalid JSON response", e)
    
    return False

def construct_project_json(): 
    entities = read_entity_types()
    # Open and load the JSON file
    with open(project_json_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        if item in entities:
            data[item] = data[item] + str(entities[item])
    
    return data
    
def create_project(body=''):
    access_token = login()
    url = str(host) +"/scp/v1/projects/update"

    parseBody =  json.loads(body)

    payload = json.dumps(parseBody)
    headers = {
      'X-auth-token': 'bearer ' + access_token,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        if response.status_code == 200:
            response_data = response.json()
            create_log("response_data")
            create_log(response_data)
            create_log("payload")
            create_log(payload)
            return response_data
        else:
            response_data = response.json()
            create_log("response_data")
            create_log(response_data)
            create_log("payload")
            create_log(payload)
            
    except ValueError as e:
        print("Invalid JSON response", e)
def create_log(resp):
    write = "a"
    if os.path.exists(response_file):
        write = "a"
    else:
        write = "w"

    API_log = open(response_file, write)
    API_log.write("\n")
    API_log.write(str(resp))
    API_log.write("\n")
    API_log.close()