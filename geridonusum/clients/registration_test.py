import requests
from pprint import pprint 

def clients():
    credentials = {
        'username' : 'rest_test_user',
        'email' : 'test@86333test.co',
        'password1' : 'smd642043?!YS',
        'password2' : 'smd642043?!YS',
    }

    response = requests.post(
        url='http://127.0.0.1:8000/api/rest-auth/registration/',
        data=credentials,
    )

    print('Status Code:', response.status_code)

    response_data = response.json()
    pprint(response_data)

if __name__ == '__main__':
    clients()
