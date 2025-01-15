import time

import requests

auth_server = 'http://127.0.0.1:5000'
resource_server = 'http://127.0.0.1:5000'

login = 'test_user'
uri1 = 'http://test_uri.ru'
uri2 = 'http://error_test_uri.ru'
client_id1 = 'xiYMmFtGOPG548JLACOCLUfq'
client_secret1 = '0t9nhvg8XrnJYwGxxpN4RMk3THwlivWExUHQ9OequKMN0gQ7'
client_id2 = 'mGwjWvKPGtmXozGomKucC3rj'	
client_secret2 = 'AWugr9GOWz0qGiRcaZeKYWPd9g6HrZEQidrRGlyfAJ5fsUJV'


def get_auth_code(client_id, redirect_uri, login):
    data = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'profile',
        'username': login,
        'confirm': 'on'
    }
    res = requests.post(f'{auth_server}/oauth/authorize', data=data, allow_redirects=False)
    url = res.headers['location']
    if 'code' in url:
        code = url[url.find('=')+1:]
    else:
        code = ''
    return code

def get_access_token(client_id, client_secret, code, redirect_uri):
    
    data = {
        'client_id': client_id, 
        'client_secret': client_secret,
        'grant_type': 'authorization_code', 
        'scope': 'profile', 
        'code': code,
        'redirect_uri': redirect_uri
    }
    res = requests.post(f'{auth_server}/oauth/token',  data=data)
    if res.status_code == 200:
        token = res.json()['access_token']
    else:
        token = ''
    return token 

def check_access(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(f'{resource_server}/api/me', headers=headers)
    return res.status_code == 200

# Подмена URI-перенаправления
def test1 (client_id, client_secret, login, uri1, uri2):
    code = get_auth_code(client_id, uri1, login)
    token = get_access_token(client_id, client_secret, code, uri2)
    if token == '':
        return True
    else:
        return False

# Повторное использование кода авторизации
def test2(client_id, client_secret, login, uri):
    code = get_auth_code(client_id, uri, login)
    get_access_token(client_id, client_secret, code, uri)
    if get_access_token(client_id, client_secret, code, uri) == '':
        return True
    else:
        return False
        

# Использование кода авторизации другим клиентом
def test3 (client_id1, client_id2, client_secret2, login, uri):
    code = get_auth_code(client_id1, uri, login)
    if get_access_token(client_id2, client_secret2, code, uri) != '':
        # Не проверяется клиент 
        return False
    else:
        return True

# Проверка времени жизни токена
def test4(client_id, client_secret, login, uri):
    code = get_auth_code(client_id, uri, login)
    token = get_access_token(client_id, client_secret, code, uri)
    time.sleep(5)
    if check_access(token) == '':
        return False
    else:
        return True

if __name__ == '__main__':
    print(test1(client_id1, client_secret1, login, uri1, uri2))
    print(test2(client_id1, client_secret1, login, uri1))
    print(test3(client_id1, client_id2, client_secret2, login, uri1))
    print(test4(client_id1, client_secret1, login, uri1))