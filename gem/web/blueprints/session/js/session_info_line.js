function InfoLine(selector) {

    var node = $(selector)

    var endTime = undefined
    var sessionTitle = undefined
    var users = undefined
    var template = Handlebars.compile($(selector).html())
    var timer = setInterval(update, 1000)

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

    // internal functions

    // renders info line
    function update() {
        var now = new Date()
        var td = timeDiff(endTime, now)
        var usersByRole = groupBy(users, "role")

        html = template({
            session: {title: sessionTitle},
            groups: usersByRole,
            users: users,
            time: td,
            timeIsUp: !(td.days || td.hours || td.minutes || td.seconds)
        })

        node.html(html)
        node.removeClass("hidden")
    }

    return { setEndTime, setUsers, setSessionTitle }
}
