// Session controller

function createSessionController(sessionKey) {
    me = {}

    me.sessionKey = sessionKey
    me.chat = createChatController(me)
    me.timer = createTimerController(me)
    me.users = createUsersController(me)
    me.manage = createManageController(me)
    me.stage = createStageController(me)


    function onKick(data) {
        me.socket.disconnect()
        showAlert("Kicked!", data.message, function () { window.location = "/" })
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
        me.socket.on("user", me.stage.onUserInfoMessage)
        me.socket.on("stage", me.stage.processMessage)
        me.socket.on("chat", me.chat.processMessage)
        me.socket.on("users", me.users.processMessage)
        me.socket.on("timer", me.timer.processMessage)
    }

    // Private members

    function showAlert(title, message, action) {
        $.alert({
            title: title,
            content: message,
            type: "red",
            buttons: {
                confirm: {
                    text: "Ok",
                    action: action
                }
            }
        })
    }

    me.connect = connect

    return me
}


$(document).ready(function() {
    var host = "http://" + document.domain + ":" + location.port
    var sessionKey = $("#session-key").text().trim()
    var controller = createSessionController(sessionKey)
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
