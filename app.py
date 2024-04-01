from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
from http import client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show():
    data = list(db.diary.find({},{'_id': False}))
    return jsonify({
        'data': data
    })

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    save_file = f'file-{mytime}.{extension}'
    filename = f'static/{save_file}'
    file.save(filename)

    profil = request.files['profil_give']
    extension = file.filename.split('.')[-1]
    save_file = f'profil-{mytime}.{extension}'
    profilname = f'static/{save_file}'
    profil.save(profilname)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'image': filename,
        'profil': profilname,
        'title':title_receive,
        'content':content_receive,
        'time': time
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)