#!/usr/bin/python3
'''Script that starts a Flask web application'''
from flask import Flask, render_template

from models import storage, State, City, Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states_id(id=None):
    '''Displays an HTML page containing a the filters bar, where "States" and\
     "Amenities" filters gets their data from the storage engine used,
    for "/hbnb_filters" route'''
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


@app.teardown_appcontext
def storage_close(exception):
    '''Teardown operations'''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
