// Session controller

function createSessionController(sessionKey, sessionData) {
    me = {}

    me.sessionKey = sessionKey
    me.users = UsersPanelController(me, $("#session-users-list"), $("#session-users-line").html())
    me.chat = createChatController(me)
    me.timer = createTimerController(me)
    me.manage = createManageController(me)
    me.stage = StageController(me, $("#stage-proposal"), $("#stage-widget"))
    me.quorum = QuorumController(me)

    // info line
    me.infoLine = InfoLineController(me, $("#footer-info"))
    me.infoLine.setEndTime(new Date(sessionData.date + " " + sessionData.time_end))
    me.infoLine.setSessionTitle(sessionData.title)


    me.user = null

    function onKick(data) {
        me.socket.disconnect()
        Alerts().alert({
            title: data.title || "You have been removed from the session",
            message: data.message
        }, function () { window.location = "/" })
    }

    function onConnected(socket) {
        $("#connection-lost").addClass("hidden")
        me.socket.emit("join", { "session": sessionKey }, onJoinResponse)
    }

    function onDisconnected(socket) {
        $("#connection-lost").removeClass("hidden")
    }

    function onReconnected(socket) {
        $("#connection-lost").addClass("hidden")
    }

    function onJoinResponse(response) {
        if (response.success != true) {
            Alerts().alert({
                title: "Error",
                message:"You are not connected to the session" },
                function () { window.location = "/" })
        }
    }

    function connect(uri) {
        me.socket = io.connect(uri)

        me.socket.on("connect", onConnected)
        me.socket.on("disconnect", onDisconnected)
        me.socket.on("reconnect", onReconnected)
        me.socket.on("kick", onKick)
        me.socket.on("user", function(data) {
            me.user=data;
            me.users.update();
        })
        me.socket.on("stage", me.stage.processMessage)
        me.socket.on("chat", me.chat.processMessage)
        me.socket.on("users", function(data) {
            me.infoLine.setUsers(data)
            me.users.setUsers(data)
        })
        me.socket.on("quorum_change_code", me.quorum.showQuorumChangeCode)
        me.socket.on("timer", me.timer.processMessage)
    }

    me.emit = function(eventName, data, response) {
        if (!response) {
            me.socket.emit(eventName, data)
        } else {
            me.socket.emit(eventName, data, response)
        }
    }

    me.connect = connect

    return me
}


$(document).ready(function() {
    var host = "http://" + document.domain + ":" + location.port
    var sessionKey = $("#session-key").text().trim()
    var sessionData = JSON.parse($("#session-data").text())
    var controller = createSessionController(sessionKey, sessionData)
    window.controller = controller

    controller.connect(host)

    Handlebars.registerPartial('agenda', $("#stage-agenda").html())
    Handlebars.registerPartial('acquaintance', $("#stage-acquaintance").html())
    Handlebars.registerPartial('voting', $("#stage-voting").html())
    Handlebars.registerPartial('votingresults', $("#stage-voting_results").html())
    Handlebars.registerPartial('commenting', $("#stage-commenting").html())
    Handlebars.registerPartial('discussion', $("#stage-discussion").html())
    Handlebars.registerPartial('closed', $("#stage-closed").html())
})
