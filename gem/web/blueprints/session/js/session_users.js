/* Manages the list of connected users.
 *
 * param session: session controller
 * param container: container to display the list of users
 * param userLineTemplate: template of user line
 */
function UsersPanelController(session, container, userLineTemplate) {

    $(document).on("click", ".kick", onKickButtonClicked)

    // Updates panel
    function update() {
        render()
    }

    // Sets list of connected users
    // param data: array of connected users
    //             [{name: "akd", role: "secretary"}, ...]
    function setUsers(data) {
        users = data
        update()
    }


    // Private members

    var users    = []
    var template = Handlebars.compile(userLineTemplate)
    var alerts   = Alerts()


    // On "kick" button clicked
    function onKickButtonClicked(e) {
        e.preventDefault()
        var userId = $(this).data("user-id")

        alerts.input("Remove user from session", "Reason", function(reason) {
            session.emit("kick", {user: userId, reason})
        })
    }

    function render() {
        container.empty()
        for (user of users) {
            container.append(template(user, {data: {user: session.user}}))
        }
    }

    return { setUsers, update }
}
