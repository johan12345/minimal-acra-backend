import json
import os
from smtplib import SMTP
from textwrap import dedent, indent

from flask import Flask, request

app = Flask(__name__)

user = os.environ['ACRA_BASIC_USER']
password = os.environ['ACRA_BASIC_PASSWORD']
smtp_host = os.environ['SMTP_HOST']
smtp_port = int(os.environ['SMTP_PORT'])
smtp_user = os.environ['SMTP_USER']
smtp_password = os.environ['SMTP_PASSWORD']
smtp_from = os.environ['SMTP_FROM']
smtp_to = os.environ['SMTP_TO']


def format(acra_data):
    text = ""
    for key in acra_data:
        text += f"{key}="
        value = acra_data[key]
        if isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
            text += str(value) + "\n"
        elif isinstance(value, list):
            text += json.dumps(value) + "\n"
        else:
            text += "\n" + indent(format(value), "  ")
    return text


@app.post('/report')
def submit_report():
    if request.authorization is None:
        return 'unauthorized', 401
    if request.authorization.username != user or request.authorization.password != password:
        return 'unauthorized', 401

    acra_data = request.get_json()

    package_name = acra_data["PACKAGE_NAME"]
    app_version_name = acra_data["APP_VERSION_NAME"]

    with SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.sendmail(
            smtp_from, smtp_to,
            dedent(f"""\
            From: {smtp_from}
            Subject: {package_name} {app_version_name} Crash Report
            
            """) + format(acra_data)
        )

    return ""


if __name__ == '__main__':
    app.run()
