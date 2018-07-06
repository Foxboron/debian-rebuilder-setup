from flask import g, render_template, Flask, Response
from os.path import join
from sqlite3 import connect

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


@app.route('/sources')
def all_sources():
    db = get_db()
    c = db.cursor()
    c.execute('SELECT source FROM BUILDS')
    results = c.fetchall()
    return render_template('all_sources.html', results=results)


@app.route('/sources/<source>')
def all_versions_of_source(source):
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM BUILDS WHERE source=?', (source,))
    results = c.fetchall()
    if len(results) == 0:
        return ('Not Found', 404, {})
    return render_template('all_versions_of_source.html', results=results)


@app.route('/sources/<source>/<version>/metadata')
def get_metadata(source, version):
    db = get_db()
    c = db.cursor()
    c.execute('SELECT metadata FROM BUILDS WHERE source=? AND version=?',
              (source, version))
    metadata = c.fetchone()
    if metadata is None:
        return ('Not Found', 404, {})
    folder_name = "%s-%s" % (source, version)
    directory = join(DIR, folder_name)
    content = open(join(directory, metadata[0])).read()
    return Response(content, mimetype='text/plain',
                    headers={
                        'Content-Disposition': 'attachment; filename="' +
                        metadata[0] + '"'
                    })


@app.route('/sources/<source>/<version>/buildinfo')
def get_buildinfo(source, version):
    db = get_db()
    c = db.cursor()
    c.execute('SELECT buildinfo FROM BUILDS WHERE source=? AND version=?',
              (source, version))
    buildinfo = c.fetchone()
    if buildinfo is None:
        return ('Not Found', 404, {})
    folder_name = "%s-%s" % (source, version)
    directory = join(DIR, folder_name)
    content = open(join(directory, buildinfo[0])).read()
    return Response(content, mimetype='text/plain',
                    headers={
                        'Content-Disposition': 'attachment; filename="' +
                        buildinfo[0] + '"'
                    })
