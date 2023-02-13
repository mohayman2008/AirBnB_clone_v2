#!/usr/bin/python3
'''Script that starts a Flask web application'''
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_id(id=None):
    '''Displays an HTML page containing a list of all the states \
    or a certain state and its cities for "/states/<id>" route'''
    states = storage.all(State)
    if id is None:
        return render_template('7-states_list.html', states=states.values())
    state = states.get('State.{}'.format(id), None)
    if state is None:
        return render_template('9-states.html', state='None')
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def storage_close(exception):
    '''Teardown operations'''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
