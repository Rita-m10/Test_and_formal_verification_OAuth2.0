import time

import requests

auth_server = 'http://127.0.0.1:5000'
resource_server = 'http://127.0.0.1:5000'

input = {'Login': 'test_user',
    'Invalid_login': 'invalid_test_user',
    'Client_id': 'xiYMmFtGOPG548JLACOCLUfq',
    'Invalid_client_id': 'vNHz3jofirf5ztniF0PayjAX',
    'Client_secret': '0t9nhvg8XrnJYwGxxpN4RMk3THwlivWExUHQ9OequKMN0gQ7',
    'Invalid_client_secret': 'uiyr834uhfyoy4uriugtgHKglTYR4UTGGF',
    'Authorization_code': '',
    'Invalid_authorization_code':'K5xH8Qkn5abv4jZr6B0eaDg1FLZoeUkfpPacRDM13M9zqytm',
    'Access_token': '',
    'Invalid_access_token': 'zAZDGvJ2nnRU8VqqLMIj40sHi6Ss7qLoyUtoUDpEgh',
    'Redirect_URI': 'http://test_uri.ru',
    'Invalid_redirect_URI': 'http://error_test_uri.ru',
    'Expires_in': 0,
    'Old_expires_in': 5
}


def home_page():
    res = requests.get(f'{auth_server}/')

def login(username):
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': username
    }
    res = requests.post(f'{auth_server}/', data=data, headers=headers)

    text = res.text
    client_id = text[text.find('client_id')+len('client_id: </strong>'):text.find('<strong>client_secret')-3]
    client_secret = text[text.find('client_secret')+len('client_secret: </strong>'):text.find('<strong>client_id_issued_at')-3]
    
    return client_id, client_secret

def get_auth_code(x, y):
    
    if x == 'Authorization_code_Request':
        data = {
            'response_type': 'code',
            'client_id': input['Client_id'],
            'redirect_uri': input['Redirect_URI'],
            'scope': 'profile',
            'username': input['Login'],
            'confirm': 'on'
        }
    if x == 'Invalid_authenticate':
        data = {
            'response_type': 'code',
            'client_id': input['Client_id'],
            'redirect_uri': input['Redirect_URI'],
            'scope': 'profile',
            'username': input['Invalid_login'],
            'confirm': 'on'
        }
    if x == 'Invalid_client_id':
        data = {
            'response_type': 'code',
            'client_id': input['Invalid_client_id'],
            'redirect_uri': input['Redirect_URI'],
            'scope': 'profile',
            'username': input['Login'],
            'confirm': 'on'
        }
    if x == 'Invalid_redirect_URI':
        data = {
            'response_type': 'code',
            'client_id': input['Client_id'],
            'redirect_uri': input['Invalid_redirect_URI'],
            'scope': 'profile',
            'username': input['Login'],
            'confirm': 'on'
        }
    if x == 'Invalid_authorization_code':
        data = {
            'code': input['Invalid_authorization_code']
        }
    if x == 'Access_Request':
        data = {
            'token': input['Access_token']
        }
    if x == 'Invalid_access_token':
        data = {
            'token': input['Invalid_access_token']
        }
    if x == 'Access_token_Request':
        data = {
            'client_id': input['Client_id'], 
            'client_secret': input['Client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Authorization_code'],
            'redirect_uri': input['Redirect_URI']
        }
    if x == 'Old_expires_in_Access_Request':
        data = {
            'expires_in': input['Old_expires_in']
        }
    if x == 'Invalid_client_secret':
        data = {
            'client_secret': input['Invalid_client_secret']
        }
    
    res = requests.post(f'{auth_server}/oauth/authorize', data=data, allow_redirects=False)

    flag = False
    if 'Location' in res.headers:
        if y in res.headers['Location']:
            flag = True
    assert (str(res.status_code) == y) or (flag == True), 'Error get_auth_code'
    if x == 'Authorization_code_Request' and flag == True:
        url = res.headers['location']
        input['Authorization_code'] = url[url.find('=')+1:]
        

def get_access_token(x, y):
    
    if x == 'Access_token_Request':
        data = {
            'client_id': input['Client_id'], 
            'client_secret': input['Client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Authorization_code'],
            'redirect_uri': input['Redirect_URI']
        }
    if x == 'Invalid_client_id':
        data = {
            'client_id': input['Invalid_client_id'], 
            'client_secret': input['Client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Authorization_code'],
            'redirect_uri': input['Redirect_URI']
        }
    if x == 'Invalid_client_secret':
        data = {
            'client_id': input['Client_id'], 
            'client_secret': input['Invalid_client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Authorization_code'],
            'redirect_uri': input['Redirect_URI']
        }
    if x == 'Invalid_authorization_code':
        data = {
            'client_id': input['Client_id'], 
            'client_secret': input['Client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Invalid_authorization_code'],
            'redirect_uri': input['Redirect_URI']
        }
    if x == 'Invalid_redirect_URI':
        data = {
            'client_id': input['Client_id'], 
            'client_secret': input['Client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Authorization_code'],
            'redirect_uri': input['Invalid_redirect_URI']
        }
    if x == 'Access_Request':
        data = {
            'token': input['Access_token']
        }
    if x == 'Invalid_access_token':
        data = {
            'token': input['Invalid_access_token']
        }
    if x == 'Authorization_code_Request':
        data = {
            'client_id': input['Client_id'],
            'redirect_uri': input['Redirect_URI'],
            'username': input['Login']
        }
    if x == 'Invalid_authenticate':
        data = {
            'username': input['Invalid_login']
        }
    if x == 'Old_expires_in_Access_Request':
        data = {
            'expires_in': input['Old_expires_in']
        }
    
    res = requests.post(f'{auth_server}/oauth/token',  data=data)

    assert res.status_code == y, 'Error get_access_token'
    if x == 'Access_token_Request':
        input['Access_token'] = res.json()['access_token']
        
    

def check_access(x, y):
    if x == 'Access_Request':
        headers = {
            'Authorization': f'Bearer {input["Access_token"]}'
        }
        data = {}
    if x == 'Old_expires_in_Access_Request':
        time.sleep(input['Old_expires_in'])
        headers = {
            'Authorization': f'Bearer {input["Access_token"]}'
        }
        data = {}
    if x == 'Invalid_access_token':
        headers = {
            'Authorization': f'Bearer {input["Invalid_access_token"]}'
        }
        data = {}
    if x == 'Authorization_code_Request':
        headers = {}
        data = {
            'client_id': input['Client_id'],
            'redirect_uri': input['Redirect_URI'],
            'username': input['Login']
        }
    if x == 'Access_token_Request':
        headers = {}
        data = {
            'client_id': input['Client_id'], 
            'client_secret': input['Client_secret'],
            'grant_type': 'authorization_code', 
            'scope': 'profile', 
            'code': input['Authorization_code'],
            'redirect_uri': input['Redirect_URI']
        }
    if x == 'Invalid_client_secret':
        headers = {}
        data = {
            'client_secret': input['Invalid_client_secret']
        }
    if x == 'Invalid_client_id':
        headers = {}
        data = {
            'client_id': input['Invalid_client_id']
        }
    if x == 'Invalid_authenticate':
        headers = {}
        data = {
            'username': input['Invalid_login']
        }
    if x == 'Invalid_redirect_URI':
        headers = {}
        data = {
            'redirect_uri': input['Invalid_redirect_URI']
        }
    if x == 'Invalid_authorization_code':
        headers = {}
        data = {
            'code': input['Invalid_authorization_code']
        }
    
    res = requests.get(f'{resource_server}/api/me', headers=headers, data=data)
    assert res.status_code == y, 'Error check_access'




if __name__ == '__main__':
    
    with open('transion.txt', 'r') as file:
        for line in file:
            transition = line.strip('\n').split(" ")
            i = 0
            
            while True:
                error = 0
                while True:
                    in_out = transition[i].split('/')
                    # Получение кода авторизации
                    get_auth_code(in_out[0], in_out[1])
                    
                    i += 1
                    if i == len(transition) or in_out[0] == 'Authorization_code_Request':
                        break
                    if in_out[0] in ['Invalid_authenticate', 'Invalid_client_id', 'Invalid_redirect_URI']:
                        error = 1
                        break
                
                if i == len(transition):
                    break
                if error == 1:
                    continue
                
                while True:
                    in_out = transition[i].split('/')
                    # Получение токена доступа
                    get_access_token(in_out[0], int(in_out[1]))
                    
                    i += 1
                    if i == len(transition) or in_out[0] == 'Access_token_Request':
                        break
                    if in_out[0] in ['Invalid_client_secret', 'Invalid_authorization_code', 'Invalid_client_id', 'Invalid_redirect_URI']:
                        error = 1
                        break
                
                if i == len(transition):
                    break
                if error == 1:
                    continue
                
                while True:
                    in_out = transition[i].split('/')
                    # Проверка доступа
                    check_access(in_out[0], int(in_out[1]))
                    
                    i += 1
                    if i == len(transition):
                        break
                    if in_out[0] in ['Old_expires_in_Access_Request', 'Invalid_access_token']:
                        error = 1
                        break
                
                if i == len(transition):
                    break
                if error == 1:
                    continue

    print("OK")
            
