import os
import io
import falcon
import requests
from datetime import datetime, timezone, timedelta
from julia import HEROKU_APP_NAME


def get_badge(name: str):
    image_path = os.path.join(os.getcwd(), f"img/{name}.svg")
    stream = io.open(image_path, "rb")
    content_length = os.path.getsize(image_path)
    return stream, content_length


class HerokuBadge:
    def on_get(self, req, resp):
        if not req.params:
            resp.content_type = "text/html"
            resp.status = falcon.HTTP_200
            with io.open("index.html", "rb") as f:
                resp.body = f.read()
                return

        app = HEROKU_APP_NAME
        path = "/"

        if not app:
            resp.status = falcon.HTTP_501
            return

        style = req.params.get("style")

        resp.cache_control = ("max-age=120",)
        resp.content_type = "image/svg+xml;charset=utf-8"
        resp.date = datetime.now(timezone.utc)
        resp.expires = datetime.now(timezone.utc) + timedelta(minutes=2)
        resp.x_dns_prefetch_control = False

        url = f"https://{app}.herokuapp.com{path}"
        try:
            r = requests.get(url, timeout=3.6)

        except requests.exceptions.Timeout:
            resp.stream, resp.content_length = get_badge(
                name="timeout")
        else:
            if r.status_code == 200:
                resp.stream, resp.content_length = get_badge(
                    name="deployed")
            elif r.status_code == 404:
                resp.stream, resp.content_length = get_badge(
                    name="not_found")
            else:
                resp.stream, resp.content_length = get_badge(
                    name="failed")


application = falcon.API()
application.add_route("/", HerokuBadge())
