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

Handlebars.registerHelper('ifEqual', function(v1, v2, options) {
    if(v1 === v2) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('percent', function(v1, v2, options) {
    return (v1 / v2 * 100) || 0;
});

Handlebars.registerHelper('ifHas', function(array, value, options) {
    var value = (array.indexOf(value) != -1)
    if (value) {
        return options.fn(this);
    }
    return options.inverse(this);
});
