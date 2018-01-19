import pdfkit
import dateutil.parser
from jinja2 import Template

from gem.db import comments, users


def print_comments(requester, criteria):
    p = "./gem/web/app/printer/"
    template_file = open(p + "comments_template.html", "r").read()
    template = Template(template_file)
    rows = map(__map, comments.find(criteria))
    html = template.render(requester=requester, rows=rows)
    pdfkit.from_string(html, "/Users/akd/Desktop/1.pdf", options={"zoom": 6})
    return "/Users/akd/Desktop/1.pdf"


def __map(r):
    r.user = users.get(r.user_id)
    if hasattr(r, "timestamp"):
        r.timestamp = dateutil.parser.parse(r.timestamp).strftime("%H:%M:%S")
    return r
