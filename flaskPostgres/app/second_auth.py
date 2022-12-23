import requests
import json

with open('config.json') as f:
    secrets = json.load(f)

email_token = secrets['key']
call_token = secrets['phone_key']


def send_code_email(email: str, name: str, code: int):
    # return
    res = requests.post(
        "https://api.mailgun.net/v3/sandbox9b05a8f6924148b28dd1a5122b44e94a.mailgun.org/messages",
        auth=("api", email_token),
        data={"from": "Mailgun Sandbox <postmaster@sandbox9b05a8f6924148b28dd1a5122b44e94a.mailgun.org>",
              "to": f"{name} <{email}>",
              "subject": f"Hello {name}! There's your code!",
              "text": f"This is your verification code – {code}"})
    return code


def send_code_call(number: int):
    url = f'https://sms.ru/code/call?phone={number}&ip=-1&api_id={call_token}'
    data = requests.post(url)
    code = json.loads(data.text)['code']
    # code = data.json['code']
    return int(code)
