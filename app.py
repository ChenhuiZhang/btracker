import os
from btracker import Map, GPX
from flask import Flask, render_template


app = Flask(__name__)
app.config['GOOGLE_KEY'] = ""
app.config['BAIDU_WEB_KEY'] = os.environ.get('BAIDU_WEB_KEY')
app.config['BAIDU_JS_KEY'] = os.environ.get('BAIDU_JS_KEY')

gpx = GPX("sample.gpx")
map = Map(gpx.trackpoints, app.config)

print(map.google_coordinates)
print(map.baidu_coordinates)
print(map.baidu_coordinates_path)


@app.route('/')
def index():
    context = {
        "key": app.config['BAIDU_JS_KEY'],
        "title": gpx.title
    }
    return render_template('bmap.html', map=map, context=context)


if __name__ == '__main__':
    app.run(debug=True)
