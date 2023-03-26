from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import RegisterForm, LoginForm
import os
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeanyvaluehere'
bootstrap = Bootstrap5(app)
stripe.api_key = os.environ.get("STRIPE_API_KEY")

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///bookshop.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """ E-commerce site User object to create User database table """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    # List of items in user's cart
    cart = relationship("Item", back_populates="buyer")


class Item(db.Model):
    """ E-commerce site Item object to store items sold on the site """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(500))
    category = db.Column(db.String(250))
    buyer = relationship("User", back_populates="cart")
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Item {self.name}>'


# Online bookshop e-commerce site
# [X] Homepage that displays some books for sale from db
# [X] Item display page for each item
# [X] View cart page
# [X] Checkout page with payment form to process payment info
# [X] Success page to show after checkout
# [X] Nav bar at upper right
# [X] Database with Items and Users
# [X] Registration form
# [X] Login page/form
# [X] Add selected item to user's cart on login
# [X] Make sure all flows clicking through the site make sense and proper behavior when user is not logged in
# [X] Button to remove from cart

db.create_all()
# Code to populate the database with books to sell if the database does not yet exist
# names = ["Used book: \"The Grapes of Wrath\" by John Steinbeck",
#          "Used book: \"The Bluest Eye\" by Toni Morrison",
#          "Used book: \"Omeros\" by Derek Walcott",
#          "Used book: \"Middlemarch\" by George Eliot",
#          "Used book: \"Harry Potter\" by J.K. Rowling",
#          "Used book: \"Americanah\" by Chimamanda Ngozie Adichie",
#          "Used book: \"A River Runs Through It\" by Norman McLean",
#          "Used book: \"The Handmaid's Tale\" by Margaret Atwood",
#          "Used book: \"I Know Why the Caged Bird Sings\" by Maya Angelou"]
# prices = [5.95, 7.99, 2.99, 3.50, 6.99, 5.96, 1.99, 3.99, 7.95]
# img_urls = ["https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1375670575i/18114322._UY475_SS475_.jpg",
#             "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1617645496l/5219.jpg",
#             "https://upload.wikimedia.org/wikipedia/en/2/2a/Omerosbook.jpg",
#             "https://images-na.ssl-images-amazon.com/images/I/81C9P6xJUwL.jpg",
#             "https://images-na.ssl-images-amazon.com/images/I/91ocU8970hL.jpg",
#             "https://www.chimamanda.com/wp-content/uploads/2021/10/Americanah-500x792-1.jpg",
#             "https://images-na.ssl-images-amazon.com/images/I/41h7rkNjOhL.jpg",
#             "https://images.booksense.com/images/818/490/9780385490818.jpg",
#             "https://cdn11.bigcommerce.com/s-5b0svc/images/stencil/1280x1280/products/2894/5177/03b8b5119c02e641ecb09fcb950493bd__29670.1595556679.jpg?c=2"]
# for i in range(9):
#     new_item = Item(id=i+1, name=names[i], price=prices[i], img_url=img_urls[i], category="used_book")
#     db.session.add(new_item)
# db.session.commit()


# Flask routes
@app.route("/")
def home():
    """ Render homepage displaying shop items """
    shop_items = Item.query.all()
    return render_template("index.html", items=shop_items)


@app.route("/item/<int:item_id>")
def display_item(item_id):
    """ Individual item details page """
    current_item = Item.query.get(item_id)
    return render_template("item.html", item=current_item)


@app.route("/add/<int:item_id>")
def add_to_cart(item_id):
    """ Add to cart page that prompts unauthenticated user to either Sign In or Register """
    cart_item = Item.query.get(item_id)
    if current_user.is_authenticated:
        current_user.cart.append(cart_item)
        db.session.commit()
        return redirect(url_for("display_cart"))
    return render_template("add-to-cart.html", cart_item=cart_item)


@app.route("/cart", defaults={'item_id': None})
@app.route("/cart/<int:item_id>")
def display_cart(item_id):
    """ Page to display current contents of user's cart """
    # Add first item to user's cart
    if item_id and current_user.is_authenticated:
        current_user.cart = [Item.query.get(item_id)]
        db.session.commit()
    # Display existing items in user's cart
    cart_items = current_user.cart
    return render_template("cart.html", cart_items=cart_items)


@app.route("/remove/<int:item_id>")
def remove_from_cart(item_id):
    """ Remove item from user's cart """
    item_to_remove = Item.query.get(item_id)
    current_user.cart.remove(item_to_remove)
    db.session.commit()
    return redirect(url_for("display_cart"))


@app.route('/register', methods=["GET", "POST"], defaults={"item_id": None})
@app.route('/register/<int:item_id>', methods=["GET", "POST"])
def register(item_id):
    """ Register new user for site """
    reg_form = RegisterForm()
    # form submitted - create new user in database
    if reg_form.validate_on_submit():
        input_email = reg_form.email.data
        # check if user already exists in database. if yes, redirect to /login
        if User.query.filter_by(email=input_email).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        hashed_salted_pwd = generate_password_hash(
            reg_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=reg_form.email.data,
            password=hashed_salted_pwd,
            name=reg_form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        # authenticate the new user with Flask-Login
        login_user(new_user)
        return redirect(url_for("display_cart", item_id=item_id))
    # else, render Register form
    return render_template("register.html", form=reg_form)


@app.route('/login', methods=["GET", "POST"], defaults={"item_id": None})
@app.route('/login/<int:item_id>', methods=["GET", "POST"])
def login(item_id):
    """ Login form for existing users """
    login_form = LoginForm()
    # if user submitted login form
    if login_form.validate_on_submit():
        found_user = User.query.filter_by(email=login_form.email.data).first()
        # check if email is valid
        if not found_user:
            flash("That email does not exist, please try again.")
        # check if password is correct
        elif not check_password_hash(found_user.password, login_form.password.data):
            flash("Incorrect password, please try again.")
        # Valid credentials - log in user with Flask-Login
        else:
            login_user(found_user)
            return redirect(url_for("display_cart", item_id=item_id))
    # else, render login form
    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    """ Log out user """
    logout_user()
    return redirect(url_for('home'))


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """ Redirect user to Stripe checkout form """
    cart_items = current_user.cart
    line_items = []
    for item in cart_items:
        line_item = {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                },
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }
        line_items.append(line_item)
    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        # _external=True arg to generate absolute URLs
        success_url=url_for("payment_success", _external=True),
        cancel_url=url_for("payment_cancel", _external=True),
    )
    return redirect(session.url, code=303)


@app.route('/success')
def payment_success():
    """ Display Success page on successful payment """
    current_user.cart = []
    db.session.commit()
    return render_template("success.html")


@app.route('/cancel')
def payment_cancel():
    """ If payment canceled, redirect to homepage """
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
