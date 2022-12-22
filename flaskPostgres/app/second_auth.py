import requests
import json

with open('config.json') as f:
    token = json.load(f)['key']


def send_code_email(email: str, name: str, code: int):
    # return
    res = requests.post(
        "https://api.mailgun.net/v3/sandbox9b05a8f6924148b28dd1a5122b44e94a.mailgun.org/messages",
        auth=("api", token),
        data={"from": "Mailgun Sandbox <postmaster@sandbox9b05a8f6924148b28dd1a5122b44e94a.mailgun.org>",
              "to": f"{name} <{email}>",
              "subject": f"Hello {name}! There's your code!",
              "text": f"This is your verification code – {code}"})
    pass
