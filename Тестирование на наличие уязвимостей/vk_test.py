import requests
import json

user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
app_id = 5739535

session = requests.Session()

headers={
    'User-Agent': user_agent_val
}


# Замена redirect_uri
def Change_redirect_uri(uri, headers):
    session = requests.Session()
    # Отправляем запрос на авторизацию через ВКонтакте
    # Выключаем автоматическую переадресацию
    req = session.get(uri, headers=headers, allow_redirects=False)
    # Выделяем адрес переадресации, на который нас должно было переадресовать
    start = req.headers['Location']
    url = start[:start.find("?")]
    url_list = start[start.find("?"):].split('&')

    # Находим state, который формирует клиент
    state = url_list[0][url_list[0].find('=')+1:]
    # Выделяем scope, т.е. области, на которые запрашивается разрешение
    scope = url_list[1][url_list[1].find('=')+1:]
    # Формируем запрос с адресом, на который нас должно было переадресовать, 
    # но меняем redirect_uri
    redirect_url = 'https://knigavuhe.org/login/social_cb/vk/'
    params1 = {
        'state': state,
        'scope': scope,
        'response_type': 'code',
        'approval_prompt': 'auto',
        'redirect_uri': redirect_url,
        'client_id': app_id
    }
    # Отправляем сформированный запрос и смотрим на код ответа
    req = session.get(url, params=params1, headers=headers, allow_redirects=True)
    print(req.text)
    return req.status_code


# Проверка на повторное использование токена авторизации (здесь это code)
def change_code(url):
    session = requests.Session()
    # Формируем запрос, в котором мы используем code и state, 
    # полученные в DevTools Firefox из соответствующего запроса 
    params = {
        'socialType': '2',
        'code': 'e765730d9a3dc0608f',
        'state': 'ee843dba70da322308b66ca9369c5809'
    }
    # Отправляем запрос
    req = session.get(url, headers=headers, params=params, allow_redirects=True)
    
    # Т.к. код ответа всегда равен 200,
    # проверяем авторизацию через вход в раздел, 
    # который доступен только авторизованному пользователю
    req = session.get('https://ficbook.net/collections/18722616', headers=headers)
    return req.status_code

if __name__ == "__main__":
    start_url = 'https://ficbook.net/social_login/2'
    print(Change_redirect_uri(start_url, headers))
    if Change_redirect_uri(start_url) != 200:
        print("Ошибка при замене redirect_uri")
    else:
        print("redirect_uri не проверяется")
    
    url = 'https://ficbook.net/social_connect'
    if change_code(url) != 200:
        print("code проверяется")
    else:
        print("code не проверяется")
  