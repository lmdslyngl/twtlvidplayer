
import json
from functools import wraps
import flask
from model import TransactionManager, Video, VideoType, Config


app = flask.Flask(__name__)


@app.after_request
def cors_header_for_debug(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:8080")
    return response


@app.route("/api/videolist", methods=["GET"])
def videolist():
    select_params = {}
    if "since_id" in flask.request.args:
        select_params["since_id"] = int(flask.request.args["since_id"])
    if "until_id" in flask.request.args:
        select_params["until_id"] = int(flask.request.args["until_id"])
    if "count" in flask.request.args:
        select_params["count"] = int(flask.request.args["count"])

    videos = Video.select(**select_params)
    videos_dict = [video.to_dict() for video in videos]
    return flask.Response(response=json.dumps(videos_dict))


@app.route("/api/videolist-until", methods=["GET"])
def videolist_until():
    select_params = {}
    if "until_id" in flask.request.args:
        select_params["until_id"] = int(flask.request.args["until_id"])
    if "count" in flask.request.args:
        select_params["count"] = int(flask.request.args["count"])

    videos = Video.select_until(**select_params)
    videos_dict = [video.to_dict() for video in videos]
    return flask.Response(response=json.dumps(videos_dict))


@app.route("/api/videolist-since", methods=["GET"])
def videolist_since():
    select_params = {}
    if "since_id" in flask.request.args:
        select_params["since_id"] = int(flask.request.args["since_id"])
    if "count" in flask.request.args:
        select_params["count"] = int(flask.request.args["count"])

    videos = Video.select_since(**select_params)
    videos_dict = [video.to_dict() for video in videos]
    return flask.Response(response=json.dumps(videos_dict))


@app.route("/api/config/<key>", methods=["GET", "POST"])
def config(key):
    if flask.request.method == "GET":
        value = Config.select(key)
        return flask.Response(response=json.dumps({"key": key, "value": value}))

    elif flask.request.method == "POST":
        value = flask.request.form["value"]
        Config.insert(key, value)
        return flask.Response(response=json.dumps({"key": key, "value": value}))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
