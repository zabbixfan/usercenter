from . import ctl as app
from flask import request
from app import logger
@app.route("/mnsback", methods=["get","post"])
def callback():
    logger().info(request.data)
    return "hello"