import configparser
import datetime
import os
import uuid

import dateutil.parser
import pdfkit
from jinja2 import Template

from gem.db import comments, users, proposals


def print_comments(requester, criteria, opts):
    conf = __config()
    zoom = conf.get("printer", "zoom", fallback=6)
    file_name = str(uuid.uuid4()) + ".pdf"
    cp = conf.get("printer", "path", fallback="files")
    path_to_printed = os.path.join(cp, file_name)
    opts = opts or {}
    anonymous = "anonymous" in opts and opts["anonymous"] is True

    proposal = None
    if "proposal_id" in criteria:
        proposal = proposals.get(criteria["proposal_id"])

    now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")

    path = os.path.abspath("gem/web/app/printer/")

    p = "./gem/web/app/printer/"
    template_file = open(p + "comments_template.html", "r").read()
    template = Template(template_file)
    rows = sorted(list(map(__map, comments.find(criteria))), key=lambda x: x.get("timestamp", ""))
    html = template.render(requester=requester, rows=rows, proposal=proposal, path=path, now=now, anonymous=anonymous)
    pdfkit.from_string(html, path_to_printed, options={"zoom": zoom})

    return {"success": True, "path": file_name}


def __map(r):
    r.user = users.get(r.user_id)
    if hasattr(r, "timestamp"):
        r.timestamp = dateutil.parser.parse(r.timestamp).strftime("%H:%M:%S")
    return r


def __config():
    config = configparser.ConfigParser()
    r = config.read("config.ini")
    return config
