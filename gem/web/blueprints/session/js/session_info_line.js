/* Manages state of information line
 *
 * param session: session controller
 * param node: node to control
 */
function InfoLineController(session, node) {

    // sets end time of the session
    // param time: session end time
    function setEndTime(time) {
        endTime = time
    }

    // sets list of users online
    // param users: list of users
    function setUsers(list) {
        users = list
    }

    // sets title
    // param title: session title
    function setSessionTitle(title) {
        sessionTitle = title
    }

    // internal members

    var endTime = new Date()
    var sessionTitle = ""
    var users = []
    var template = Handlebars.compile("{{> info_line }}")
    var timer = setInterval(update, 1000)

    // renders info line
    function update() {
        var now = new Date()
        var td = timeDiff(now, endTime)
        var usersByRole = groupBy(users, "role")
        var fiveMinutes = 1000 * 60 * 5

        node.html(template({
            session: {title: sessionTitle},
            groups: usersByRole,
            users: users,
            time: td,
            style: td.negative ? "danger" : td.distance < fiveMinutes ? "warning" : "primary",
            overtime: td.negative
        }))

        node.removeClass("hidden")
    }

    return { setEndTime, setUsers, setSessionTitle }
}
