import json

from flask import *

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def hello_world():
    data = request.
    print(data)
    print(3)
    headers = {
        "Allow-Origin": "*",
        "Access-Control-Allow-Origin": "*",
    }
    response = Response(status=200, headers=headers)
    return response

app.run(host='192.168.1.64', port=5000)
