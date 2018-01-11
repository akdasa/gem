// Session controller

function createSessionController(sessionKey, sessionData) {
    me = {}

    me.sessionKey = sessionKey
    me.users = UsersPanelController(me, $("#session-users-list"), $("#session-users-line").html())
    me.chat = createChatController(me)
    me.timer = createTimerController(me)
    me.manage = createManageController(me)
    me.stage = createStageController(me)

    // info line
    me.infoLine = InfoLine("#footer-info")
    me.infoLine.setEndTime(new Date(sessionData.date + " " + sessionData.time_end))
    me.infoLine.setSessionTitle(sessionData.title)


    me.user = null

    function onKick(data) {
        me.socket.disconnect()
        Alerts().alert("You have been removed from the session", data.message, function () { window.location = "/" })
    }

    function onConnected(socket) {
        $("#connection-lost").addClass("hidden")
        me.socket.emit("join", { room: sessionKey })
    }

    function onDisconnected(socket) {
        $("#connection-lost").removeClass("hidden")
    }

    function onReconnected(socket) {
        $("#connection-lost").addClass("hidden")
    }

    function connect(uri) {
        me.socket = io.connect(uri)

        me.socket.on("connect", onConnected)
        me.socket.on("disconnect", onDisconnected)
        me.socket.on("reconnect", onReconnected)
        me.socket.on("kick", onKick)
        me.socket.on("user", function(data) {
            me.user=data;
            me.stage.onUserInfoMessage(data);
            me.users.update();
        })
        me.socket.on("stage", me.stage.processMessage)
        me.socket.on("chat", me.chat.processMessage)
        me.socket.on("users", function(data) {
            me.infoLine.setUsers(data)
            me.users.setUsers(data)
        })
        me.socket.on("timer", me.timer.processMessage)
    }

    me.emit = function(eventName, data) {
        me.socket.emit(eventName, data)
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
