import urllib
from flask import Flask, request, send_from_directory, redirect, url_for, send_file
from api import *

getBookInformationAPIList = [getBookInformationAPI1, getBookInformationAPI2, getBookInformationAPI3]

app = Flask(__name__)


@app.route('/getBook')
def get_book():
    url = request.args.get('url')
    url = urllib.parse.unquote(url)
    isNoChapterIndex = request.args.get('is_no_chapter_index')
    isNoChapterIndex = True if isNoChapterIndex == 'true' or 'True' else False
    title, writer, introduction, content = getBookInformationAPIList[1](url, isNoChapterIndex)
    makeEbook(title, writer, introduction, content)
    return send_from_directory('', title + '.epub')


@app.route('/updateCover', methods=['POST'])
def update_cover():
    uploaded_file = request.files['file']
    uploaded_file.save('cover.jpg')
    return redirect(url_for('home'))


@app.route('/')
def home():
    return send_file('index.html')


@app.route('/main.js')
def main_js():
    return send_file('main.js')


@app.route('/style.css')
def style():
    return send_file('style.css')


if __name__ == '__main__':
    app.run()
