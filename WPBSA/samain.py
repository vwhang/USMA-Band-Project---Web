from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from werkzeug import secure_filename
import sentimentanalysis as sa

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'csvs')


app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename('useruploadeddata.csv')
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('file uploaded successfully, Please Refresh Page')
        return redirect(url_for('index'))
    else:
        return render_template('upload.html')


@app.route('/', methods=['GET', 'POST'])
def index():

    return(render_template('index.html'))


@app.route('/get_score', methods=['GET', 'POST'])
def get_score():
    my_list = sa.get_comments()
    # print(type(my_list))
    word_score = sa.split_string(my_list)
    avg_val = sa.calculate_value(word_score)
    return(render_template('score.html', score=avg_val))


@app.route('/about/')
def about_project():

    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
