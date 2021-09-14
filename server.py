import logging
import time

from flask import Flask, request, jsonify
from healthcheck import HealthCheck
import sentry_sdk

from text_detection_v1 import get_text_detection_v1

logger = logging.getLogger(__name__)

app = Flask(__name__)
health = HealthCheck(app, "/healthcheck")
logging.getLogger("werkzeug").setLevel("WARNING")


@app.route("/respond", methods=["POST"])
def respond():
    st_time = time.time()

    image = request.json.get("image", "")
    east = request.json.get("east", "")
    min_confidence = request.json.get("min_confidence", 0)
    width = request.json.get("width", 0)
    height = request.json.get("width", 0)

    args = {"image": image, "east": east, "min_confidence": min_confidence, "width": width, "height": height}
    
    logger.info(f"got request: image={image}, east={east}, min_confidence={min_confidence}, width={width}, height={height}")

    try:
        result = get_text_detection_v1(args)
    except Exception as exc:
        logger.exception(exc)
        sentry_sdk.capture_exception(exc)
        result = []

    total_time = time.time() - st_time
    logger.info(f"zero-shot object detection exec time: {total_time:.3f}s")
    return jsonify(result)