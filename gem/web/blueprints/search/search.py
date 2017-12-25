from flask import Blueprint, render_template, request
from flask_login import login_required

from gem.db import laws

search = Blueprint("search", __name__, template_folder=".")


@search.route("/")
@login_required
def search_results():
    q = request.args.get("q", None)
    sr = laws.find({"$text": {
        "$search": q
    }})
    sr = map(lambda x: {
        "title": x.title,
        "matches": list(__highlight(x.content, q))[:5],
        "link": "/laws/" + str(x["_id"])
    }, list(sr))

    return render_template("search_results.html", q=q, results=list(sr))


def __highlight(line, q):
    import re
    result = [(a.start(), a.end()) for a in list(re.finditer(q, line))]
    result = map(lambda x: line[x[0]-150:x[1]+150], result)
    result = map(lambda x: x.replace(q, "<span class='search-highlight'>" + str(q) + "</span>"), result)
    return result
