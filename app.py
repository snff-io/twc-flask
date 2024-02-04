from flask import Flask, render_template, g
import server.user
import server.canvas_map
import storage.iching_class
import storage.iching_model
app = Flask(__name__)

@app.before_first_request
def before_first_request():
    g.icc = storage.iching_class.IChing()

@app.route("/")
def index():
    return render_template("index.html", title="Hello")

userApi = server.user.user_api("Hello from the API!")
@app.route("/api/v1/user")
def api_index():
    return userApi.get_hello_api()


@app.route("/map")
def map():
    return server.canvas_map.HexagramGrid(100, 100).render()
