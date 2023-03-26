from flask_bootstrap import Bootstrap5
from flask import render_template, redirect, url_for
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeanyvaluehere'
bootstrap = Bootstrap5(app)
BASE_URL = "https://api.paperquotes.com/apiv1"
PAPER_API_KEY = ""
HEADERS = {
    "Authorization": f"Token {PAPER_API_KEY}"
}


# Quote Generator website
# Homepage: display Quote of the Day
# Search by tag and click through pages of search results
# TODO - Upvote/downvote a quote


class SearchForm(FlaskForm):
    """ FlaskForm for searching quotes by tag """
    search_tag = SelectField(coerce=str, validators=[DataRequired()])
    submit = SubmitField("Search")


# Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    """ Render homepage with Quote of the Day and quote search form """
    qod_url = f"{BASE_URL}/qod"
    params = {
        "language": "en"
    }
    qod_response = requests.get(qod_url,
                            params=params,
                            headers=HEADERS).json()
    quote = qod_response.get("quote")
    author = qod_response.get("author")
    pk = qod_response.get("pk")
    tags_url = f"{BASE_URL}/tags/"
    params = {
        "limit": 20
    }
    tags_response = requests.get(tags_url,
                                 headers=HEADERS,
                                 params=params).json()
    tags_results = tags_response.get("results")
    tags_choices = ["Select..."] + [result.get("name") for result in tags_results]
    search_form = SearchForm()
    search_form.search_tag.choices = tags_choices
    # search form submitted
    if search_form.validate_on_submit():
        search_tag = search_form.search_tag.data
        return redirect(url_for("search_quotes_by_tag",
                                tag=search_tag, offset=1))
    # otherwise, render homepage
    return render_template("index.html",
                           quote=quote, author=author,
                           pk=pk, form=search_form)


@app.route("/search/<tag>/<int:offset>")
def search_quotes_by_tag(tag, offset):
    """ Search quotes by tag and display 5 quotes at a time """
    quotes_by_tag_url = f"{BASE_URL}/quotes/"
    params = {
        "tags": tag,
        "order": "-likes",
        "offset": offset
    }
    response = requests.get(quotes_by_tag_url,
                            headers=HEADERS,
                            params=params).json()
    results = response.get("results")
    quote_data = [{"quote": quote.get("quote"),
                   "author": quote.get("author"),
                   "likes": quote.get("likes"),
                   "pk": quote.get("pk")} for quote in results]
    return render_template("quotes.html", tag=tag.title(),
                           quotes=quote_data, offset=offset)


@app.route("/next/<tag>/<int:old_offset>")
def next_page(tag, old_offset):
    """ Advance to next page of quote search results """
    tag = tag.lower()
    new_offset = old_offset + 5
    return redirect(url_for("search_quotes_by_tag",
                            tag=tag, offset=new_offset))


@app.route("/prev/<tag>/<int:old_offset>")
def prev_page(tag, old_offset):
    """ Return to previous page of quote search results """
    tag = tag.lower()
    new_offset = old_offset - 5
    return redirect(url_for("search_quotes_by_tag",
                            tag=tag, offset=new_offset))


# TODO Get following upvote and downvote functions working
# > They currently do not work. Awaiting response from Paper Quotes API developers.
@app.route("/upvote/<quote_id>")
def upvote_quote(quote_id):
    """ Upvote a quote """
    upvote_url = f"{BASE_URL}/upvote/"
    req_data = {
        "pk": quote_id
    }
    response = requests.post(upvote_url,
                             headers=HEADERS,
                             data=req_data)
    response.raise_for_status()


@app.route("/downvote/<quote_id>")
def downvote_quote(quote_id):
    """ Downvote a quote """
    upvote_url = f"{BASE_URL}/downvote/"
    req_data = {
        "pk": quote_id
    }
    response = requests.post(upvote_url,
                             headers=HEADERS,
                             data=req_data)
    response.raise_for_status()


if __name__ == '__main__':
    app.run(debug=True)
