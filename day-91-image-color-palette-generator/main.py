from flask_bootstrap import Bootstrap5
from flask import render_template, redirect, url_for
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from matplotlib import image as pltimg
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeanyvaluehere'
bootstrap = Bootstrap5(app)

UPLOADS_DIR = "uploads/"


# Helper functions
def process_image(img_file):
    """ Process image file as numpy ndarray and return list of arrays represented top 10 most common colors in image
    :param str img_file: Image file path
    :return: Top 10 colors in image as list of [R, G, B] value arrays
    """
    # get image as numpy 3d array
    image = pltimg.imread(img_file)
    # transform array by vertically stacking into list of pixels of form [R, G, B]
    pixels_rgb = np.vstack(image)
    # get pixel values and their counts
    values, counts = np.unique(pixels_rgb, return_counts=True, axis=0)
    # get indices of top 10 most frequent pixel values
    idx_top_10_counts = np.argpartition(-counts, kth=10)[:10]
    # get top 10 most frequent pixel values and return
    top_10_vals = values[idx_top_10_counts]
    # handle case where there is a 4th value for opacity in each RGB array
    top_10_vals = [arr[:3] for arr in top_10_vals]
    # handle case where color number codes are from 0-1 instead of 0-255
    if top_10_vals[0][0] <= 1:
        for i in range(len(top_10_vals)):
            for j in range(len(top_10_vals[i])):
                top_10_vals[i][j] = int(top_10_vals[i][j] * 256)
            # convert floats to ints
            top_10_vals[i] = top_10_vals[i].astype(int)
    return top_10_vals


def convert_rgb_to_hex(rgb_list):
    """
    Convert list of RGB arrays to hex color codes to display both on webpage
    :param list rgb_list: List of RGB color codes to convert as list of [R, G, B] arrays
    :return: Array of hex value strings
    """
    hex_vals = []
    for r, g, b in rgb_list:
        hex_vals.append('#%02x%02x%02x' % (r, g, b))
    return hex_vals


class UploadForm(FlaskForm):
    """ FlaskForm for uploading image files to process """
    file = FileField(validators=[DataRequired()])
    submit = SubmitField("Upload")


# Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    """ Render homepage with upload form """
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.data.get('file').filename)
        form.file.data.save(f"static/{UPLOADS_DIR}{filename}")
        return redirect(url_for('display_image', filename=filename))
    return render_template("index.html", form=form)


@app.route("/image/<filename>")
def display_image(filename):
    """ Display image with its top 10 colors """
    top_color_rgb_vals = process_image(f"static/{UPLOADS_DIR}{filename}")
    hex_vals = convert_rgb_to_hex(top_color_rgb_vals)
    colors = zip(top_color_rgb_vals, hex_vals)
    return render_template("image.html",
                           img_filename=f"{UPLOADS_DIR}{filename}",
                           colors=colors)


if __name__ == '__main__':
    app.run(debug=True)
