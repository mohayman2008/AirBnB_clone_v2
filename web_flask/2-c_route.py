#!/usr/bin/python3
'''Script that starts a Flask web application'''
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    '''Display “Hello HBNB!” for the root "/" route'''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Display “HBNB” for "/hbnb" route'''
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    '''Display “C is <text>” for "/c/<text>" route'''
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
