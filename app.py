import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def wordcount(filename, find_word):
    file = open(app.config['UPLOAD_FOLDER'] + filename, 'r').read()
    count = 0
    words = file.split()
    for word in words:
        if(word == find_word):
            count += 1
    return count

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        word = request.form['word']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            count = str(wordcount(filename, word))
            os.remove(app.config['UPLOAD_FOLDER'] + filename)
            return render_template('index.html',
                                   filename = filename,
                                   word = word,
                                   count = count)

    return render_template('index.html', count = None)

if __name__ == "__main__":
    if(not os.path.isdir(app.config['UPLOAD_FOLDER'])):
        os.makedirs(app.config['UPLOAD_FOLDER']) #Create upload-folder if it does not exist

    app.run(host='localhost', debug = True) # Start the app