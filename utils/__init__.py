import re
import warnings
import altair as alt
import json
import numpy as np
warnings.filterwarnings("ignore")


def get_chart(data, x_label, y_label, title):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title=title)
        .mark_line()
        .encode(
            x=x_label,
            y=y_label,
            color="symbol",
            strokeDash="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=x_label,
            y=y_label,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(x_label, title="Date"),
                alt.Tooltip(y_label, title=y_label),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


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
