from flask import Flask, flash, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os

from find_colors import FindColors

UPLOAD_FOLDER = 'static/uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.urandom(24)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)

        color_list = []
        colors = FindColors(file).find_colors()
        for color in colors:
            color_list.append(color.split()[-1].lstrip('(').rstrip(')'))
        dominant = FindColors(file).find_dominant_color().split()[-1].lstrip('(').rstrip(')')
        num_colors = len(color_list)
        print(color_list)
        flash('Upload Successful')

        return render_template('upload.html',
                               filename=filename,
                               colors=color_list,
                               dominant=dominant,
                               num_colors=num_colors)
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)
