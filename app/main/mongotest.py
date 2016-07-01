# coding=utf-8
import flask
import pymongo
import bson.binary
from cStringIO import StringIO
from PIL import Image
allow_formats = set(['jpeg', 'png', 'gif'])

app = flask.Flask(__name__)
app.debug = True
db = pymongo.MongoClient('172.16.124.10', 27017).test2

def save_file(f):
    content = StringIO(f.read())
    try:
        mime = Image.open(content).format.lower()
        if mime not in allow_formats:
            raise IOError()
    except IOError:
        flask.abort(400)
    c = dict(bug_id='Bug201606291504100001',
            filename=f.filename,
            content=bson.binary.Binary(content.getvalue()),
            mime=mime)
    db.files.save(c)
    return c['_id']

@app.route('/f/<fid>')
def serve_file(fid):
    try:
        f = db.files.find_one(bson.objectid.ObjectId(fid))
        if f is None:
            raise bson.errors.InvalidId()
        return flask.Response(f['content'], mimetype='image/' + f['mime'])
    except bson.errors.InvalidId:
        flask.abort(404)

@app.route('/upload', methods=['POST'])
def upload():
    f = flask.request.files['uploaded_file']
    fid = save_file(f)
    return flask.redirect( '/f/' + str(fid))

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <body>
    <form action='/upload' method='post' enctype='multipart/form-data'>
     <input type='file' name='uploaded_file'>
     <input type='submit' value='Upload'>
    </form>
    '''


if __name__ == '__main__':
    app.run(port=7777)

