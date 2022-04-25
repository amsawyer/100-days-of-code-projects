from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, unique=False, default=False)
    has_wifi = db.Column(db.Boolean, unique=False, default=False)
    has_sockets = db.Column(db.Boolean, unique=False, default=False)
    can_take_calls = db.Column(db.Boolean, unique=False, default=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    open_time = db.Column(db.String(250))
    close_time = db.Column(db.String(250))

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


## HTTP GET - Read Record

@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return jsonify([cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search_cafes():
    loc = request.args.get('loc')
    cafe_in_loc = db.session.query(Cafe).filter_by(location=loc).all()
    if not cafe_in_loc:
        return jsonify(error={
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        )
    return jsonify([cafe.to_dict() for cafe in cafe_in_loc])


## HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_cafe_to_db():
    body = request.form

    new_cafe = Cafe(
        name=body.get("name"),
        map_url=body.get("map_url"),
        img_url=body.get("img_url"),
        location=body.get("location"),
        seats=body.get("seats"),
        # convert strings to booleans
        has_toilet=body.get("has_toilet") == "True",
        has_wifi=body.get("has_wifi") == "True",
        has_sockets=body.get("has_sockets") == "True",
        can_take_calls=body.get("can_take_calls") == "True",
        coffee_price=body.get("coffee_price"),
        open_time=body.get("open_time"),
        close_time=body.get("close_time")
    )
    try:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    except exc.IntegrityError:
        return jsonify(error={"Server Error": "Cafe was not added."})


## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_coffee_price(cafe_id):
    cafe_to_update = db.session.query(Cafe).get(cafe_id)
    if cafe_to_update:
        new_price = request.args.get("new_price")
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404


## HTTP DELETE - Delete Record

@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def report_cafe_closed(cafe_id):
    cafe_to_delete = db.session.query(Cafe).get(cafe_id)
    # cafe found - delete it
    if cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    # cafe not found
    else:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
