from debian.deb822 import Deb822
from flask import g, request, Flask
from os import mkdir
from os.path import join
from sqlite3 import connect
from time import time

app = Flask(__name__)

DIR = "/var/builds/"
DATABASE = '/var/rebuilder.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/new_build', methods=['POST'])
def new_build():
    metadata = request.files['metadata']
    buildinfo = request.files['buildinfo']
    source = None
    version = None
    for paragraph in Deb822.iter_paragraphs(buildinfo):
        for item in paragraph.items():
            if item[0] == 'Source':
                source = item[1]
            if item[0] == 'Version':
                version = item[1]
    buildinfo.seek(0)
    folder_name = "%s-%s" % (source, version)
    directory = join(DIR, folder_name)
    mkdir(directory)
    timestamp = time()
    metadata.save(join(directory, metadata.filename))
    buildinfo.save(join(directory, buildinfo.filename))
    db = get_db()
    c = db.cursor()

    c.execute('INSERT INTO BUILDS VALUES (?, ?, ?, ?, ?)',
              (source, version, timestamp,
               metadata.filename, buildinfo.filename)
              )

    db.commit()
    return "OK"
