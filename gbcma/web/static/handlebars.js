Handlebars.registerHelper('trimString', function(passedString, length) {
    if (passedString.length > length) {
        var theString = passedString.substring(0, length) + "..."
        return new Handlebars.SafeString(theString)
    } else {
        return passedString
    }
});
