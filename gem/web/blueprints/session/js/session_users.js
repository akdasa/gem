/* Manages the list of connected users. */
function createUsersController(controller) {

    // Processes incoming message
    // param: data - array of connected users
    //        [{name: "akd", role: "secretary"}, ...]
    function processMessage(data) {
        render(data)
    }

    // Private members

    var panel    = $("#session-users-list")
    var line     = "<li>{{name}} <small>{{role}}</small></li>"
    var template = Handlebars.compile(line)


    function render(users) {
        panel.empty()
        for (user of users) {
            panel.append(template(user))
        }
    }

    return { processMessage }
}
