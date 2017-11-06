Handlebars.registerHelper('trimString', function(passedString, length) {
    if (passedString.length > length) {
        var theString = passedString.substring(0, length) + "..."
        return new Handlebars.SafeString(theString)
    } else {
        return passedString
    }
});

Handlebars.registerHelper('thumbsIcon', function(type) {
    if (type == "info") return "glyphicon-info-sign";
    if (type == "plus") return "glyphicon-thumbs-up";
    if (type == "minus") return "glyphicon-thumbs-down";
});
