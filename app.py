import os
from btracker import Map, GPX
from flask import Flask, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['GOOGLE_KEY'] = ""
app.config['BAIDU_WEB_KEY'] = os.environ.get('BAIDU_WEB_KEY')
app.config['BAIDU_JS_KEY'] = os.environ.get('BAIDU_JS_KEY')



@app.route('/')
def index():
    context = {
        "title": "Sample"
    }
    return render_template('index.html', context=context)

@app.route('/upload', methods=['POST'])
def upload():
    gpx = request.files['gpx_file']
    if gpx:
        print(gpx.filename)
        new_filename = secure_filename(gpx.filename)
        gpx.save(new_filename)

    return redirect(url_for('map', filename=new_filename))
    #return render_template('index.html', context={ "title": gpx.filename })

@app.route('/map?filename=<filename>')
def map(filename):
    print(filename);
    gpx = GPX(filename)
    map = Map(gpx.trackpoints, app.config)

    print(map.google_coordinates)
    print(map.baidu_coordinates)
    print(map.baidu_coordinates_path)

    context = {
        "key": app.config['BAIDU_JS_KEY'],
        "title": gpx.title
    }
    return render_template('bmap.html', map=map, context=context)


if __name__ == '__main__':
    app.run(debug=True)
