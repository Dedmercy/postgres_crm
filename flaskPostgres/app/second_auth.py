import requests


def send_code_email(email: str, name: str, code: int):
    # return
    requests.post(
        "https://api.mailgun.net/v3/sandboxef94a3dc8bcb489e909ce440d768e09e.mailgun.org/messages",
        auth=("api", "ce9e3dc031adbda06584f64bdf9ad95b-eb38c18d-57e3e233"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxef94a3dc8bcb489e909ce440d768e09e.mailgun.org>",
              "to": email,
              "subject": f"Hello {name}! There's your code!",
              "text": f"This is your verification code – {code}"})
