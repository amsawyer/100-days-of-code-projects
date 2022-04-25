from flask import render_template, redirect, url_for
import requests
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Optional, URL
# Flask app is imported from rest_api.py file
from rest_api import *

app.config['SECRET_KEY'] = 'placeanyvaluehere'
Bootstrap(app)

BASE_URL = "http://localhost:5000"
ORDERED_COLS = {"img_url": "Cafe Image",
                "name": "Cafe Name",
                "map_url": "Map URL",
                "location": "Cafe Location",
                "seats": "Number of Seats",
                "has_toilet": "Has toilet?",
                "has_wifi": "Has WiFi?",
                "has_sockets": "Has power sockets?",
                "can_take_calls": "Can take calls?",
                "coffee_price": "Coffee Price",
                "open_time": "Opening Time",
                "close_time": "Closing Time"}
LOC_CHOICES = [None,
               "Bankside",
               "Barbican",
               "Bermondsey",
               "Borough",
               "Clerkenwell",
               "Hackney",
               "London Bridge",
               "Missoula",
               "New York",
               "Paris",
               "Peckham",
               "Shoreditch",
               "South Kensington",
               "Whitechapel"]


# Site design: 3 pages
# 1. Homepage - Horizontal row of buttons
    # 'I'm Feeling Lucky' random selection button
    # All Cafes button - Link to Cafes page (item 2 in this list)
    # Search by Location dropdown
    # Add New Cafe button at bottom right
# 2. Cafes page - Display all cafes by default
    # Search by Location dropdown at upper right
    # Update price button next to each coffee price
    # Return to Home and Add New Cafe buttons at bottom
    # Delete 'X' on right side of each row
# 3. Add New Cafe form page


class SearchForm(FlaskForm):
    loc = SelectField('Cafe Location', choices=LOC_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Search by Location")


class UpdateCoffeePriceForm(FlaskForm):
    new_price = StringField('New Coffee Price', validators=[DataRequired()])
    cafe_id = HiddenField(label=None)
    submit = SubmitField("Update")


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Cafe Google Maps URL', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image URL', validators=[Optional(), URL()])
    location = SelectField('Cafe Location', choices=LOC_CHOICES, validators=[DataRequired()])
    seats = StringField('Number of Seats', validators=[DataRequired()])
    has_toilet = BooleanField('Has toilet?')
    has_wifi = BooleanField('Has WiFi?')
    has_sockets = BooleanField('Has power sockets?')
    can_take_calls = BooleanField('Good place to take calls?')
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    open_time = StringField('Opening Time')
    close_time = StringField('Closing Time')
    submit = SubmitField('Submit')


def display_search_by_loc_results(submitted_search_form):
    """ Helper function to display the cafe(s) matching location search. """
    new_search_form = SearchForm()
    update_price_form = UpdateCoffeePriceForm()
    search_loc = submitted_search_form.loc.data
    if search_loc == "None":
        loc_cafes = requests.get(f"{BASE_URL}/all").json()
    else:
        params = {"loc": search_loc}
        loc_cafes = requests.get(f"{BASE_URL}/search",
                                 params=params).json()
    if 'error' in loc_cafes:
        loc_cafes = []
    return render_template('cafes.html',
                           cafes=loc_cafes,
                           cols=ORDERED_COLS,
                           search_form=new_search_form,
                           update_form=update_price_form)


# all Flask routes below
@app.route("/", methods=["GET", "POST"])
def home():
    """ Homepage """
    search_form = SearchForm()
    # search form submitted
    if search_form.validate_on_submit():
        return display_search_by_loc_results(search_form)
    # render homepage
    return render_template("index.html", search_form=search_form)


@app.route('/random_cafe')
def random_cafe():
    """ Get random coffee shop for 'I'm Feeling Lucky' button """
    search_form = SearchForm()
    update_price_form = UpdateCoffeePriceForm()
    rand_cafe = [requests.get(f"{BASE_URL}/random").json().get('cafe')]
    return render_template('cafes.html',
                           cafes=rand_cafe,
                           cols=ORDERED_COLS,
                           search_form=search_form,
                           update_form=update_price_form)


@app.route('/cafes', methods=["GET", "POST"])
def cafes():
    """ Display all coffee shops in table """
    all_cafes = requests.get(f"{BASE_URL}/all").json()
    search_form = SearchForm()
    update_price_form = UpdateCoffeePriceForm()
    # search form submitted
    if search_form.validate_on_submit():
        return display_search_by_loc_results(search_form)
    if update_price_form.validate_on_submit():
        params = {
            "new_price": update_price_form.data['new_price']
        }
        requests.patch(f"{BASE_URL}/update-price/{update_price_form.data['cafe_id']}",
                       params=params)
        return redirect(url_for('cafes'))
    return render_template('cafes.html',
                           cafes=all_cafes,
                           cols=ORDERED_COLS,
                           search_form=search_form,
                           update_form=update_price_form)


@app.route('/add_cafe', methods=["GET", "POST"])
def add_cafe():
    """ Add new coffee shop to the database """
    form = CafeForm()
    # form submitted
    if form.validate_on_submit():
        requests.post(f"{BASE_URL}/add", data=form.data)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/delete_cafe/<cafe_id>')
def delete_cafe(cafe_id):
    """ Delete a coffee shop from the database """
    requests.delete(f"{BASE_URL}/report-closed/{cafe_id}")
    return redirect(url_for('cafes'))


@app.route("/api")
def api_docs():
    """ Display link to REST API documentation """
    return render_template("api.html")


if __name__ == '__main__':
    app.run(debug=True)
