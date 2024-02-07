#!/usr/bin/python3
'''Script that starts a Flask web application'''
from flask import Flask, render_template

from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def states_id(id=None):
    '''Displays the AirBnB clone index page, with the data loadedd from \
    the used storage engine used, for "/hbnb" route'''
    data = {'states': storage.all(State).values(),
            'amenities': storage.all(Amenity).values(),
            'places': storage.all(Place).values()}
    return render_template('100-hbnb.html', **data)


@app.teardown_appcontext
def storage_close(exception):
    '''Teardown operations'''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
