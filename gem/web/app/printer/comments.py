import pdfkit
import dateutil.parser
import configparser
from jinja2 import Template

from gem.db import comments, users


def print_comments(requester, criteria):
    conf = __config()
    path_to_printed = conf.get("[printer]", "path", fallback="temp/printed")

    p = "./gem/web/app/printer/"
    template_file = open(p + "comments_template.html", "r").read()
    template = Template(template_file)
    rows = map(__map, comments.find(criteria))
    html = template.render(requester=requester, rows=rows)
    pdfkit.from_string(html, path_to_printed + "/1.pdf", options={"zoom": 6})
    return path_to_printed + "/1.pdf"


def __map(r):
    r.user = users.get(r.user_id)
    if hasattr(r, "timestamp"):
        r.timestamp = dateutil.parser.parse(r.timestamp).strftime("%H:%M:%S")
    return r

def __config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config
