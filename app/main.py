import os

from flask import Flask, request

app = Flask(__name__)

user = os.environ['ACRA_BASIC_USER']
password = os.environ['ACRA_BASIC_PASSWORD']


@app.post('/report')
def submit_report():
    if request.authorization is None:
        return 'unauthorized', 401
    if request.authorization.username != user or request.authorization.password != password:
        return 'unauthorized', 401

    request_data = request.get_json()
    print(request_data)

    # TODO: send email

    return ""


if __name__ == '__main__':
    app.run()
