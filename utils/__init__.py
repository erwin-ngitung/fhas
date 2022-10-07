import re
import warnings
import altair as alt
import json
import numpy as np
warnings.filterwarnings("ignore")


def update_json(name, username, email, password):
    data = open('dataset/data_email.json')

    data_email = json.load(data)

    name = data_email['name'] + [name]
    username = data_email['username'] + [username]
    email = data_email['email'] + [email]
    password = data_email['password'] + [password]

    data.close()

    data_email = {'name': name,
                  'username': username,
                  'email': email,
                  'password': password}

    with open('dataset/data_email.json', 'w') as json_file:
        json.dump(data_email, json_file)

    return None


def check_account(name_email, name_password):
    data = open('dataset/data_email.json')

    data_email = json.load(data)

    name = data_email['name']
    username = data_email['username']
    email = data_email['email']
    password = data_email['password']

    index = np.where(np.array(email) == name_email)[0][0]
    password_true = password[index]

    if name_email in email and name_password == password_true:
        return name[index], username[index], 'register'
    if name_email in email and name_password != password_true:
        return '', '', 'wrong password'
    if name_email not in email:
        return '', '', 'not register'


def check_email(email):
    data = open('dataset/data_email.json')

    data_email = json.load(data)

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email):
        if email not in data_email['email']:
            value = "valid email"
        else:
            value = "duplicate email"
    else:
        value = "invalid email"

    return value
