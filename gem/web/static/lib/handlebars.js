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

Handlebars.registerHelper('percentRound', function(v1, v2, options) {
    var decimals = 1;
    var value = (v1 / v2 * 100) || 0;
    return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
});

Handlebars.registerHelper('percent', function(v1, v2, options) {
    return (v1 / v2 * 100) || 0;
});

Handlebars.registerHelper('ifHas', function(array, value, options) {
    if (array) {
        var value = (array.indexOf(value) != -1)
        if (value) {
            return options.fn(this);
        }
    }
    return options.inverse(this);
});

Handlebars.registerHelper('has', function(array, value, options) {
    var value = (array.indexOf(value) != -1)
    if (value) {
        return true;
    }
    return false;
});

Handlebars.registerHelper('list', function(array) {
    return array.join(", ");
});

Handlebars.registerHelper('len', function(array) {
    return array.length;
});

Handlebars.registerHelper('extract', function(array, field) {
    return array.map(function(x) { return x[field] })
});

Handlebars.registerHelper({
    eq: function (v1, v2) {
        return v1 === v2;
    },
    ne: function (v1, v2) {
        return v1 !== v2;
    },
    lt: function (v1, v2) {
        return v1 < v2;
    },
    gt: function (v1, v2) {
        return v1 > v2;
    },
    lte: function (v1, v2) {
        return v1 <= v2;
    },
    gte: function (v1, v2) {
        return v1 >= v2;
    },
    and: function (v1, v2) {
        return v1 && v2;
    },
    or: function (v1, v2) {
        return v1 || v2;
    },
    not: function (v1) {
        return !v1;
    }
});