function createSessionController(sessionKey) {
    var me = {
        sessionKey: sessionKey,
        stageTemplate: Handlebars.compile($("#stage-template").html())
    }

    // Handlers --------------------------------------------------------------------------------------------------------

    me.onUsersListMessage = function(data) {
        me._renderUsersList(data)
    }

    me.onChatMessage = function(data) {
        me._appendChatMessage(data)
    }

    me.onStageMessage = function(data) {
        console.log(data)
        me._renderStage(data)
    }

    me.onConnected = function(socket) {
        me.socket.emit("join", { room: me.sessionKey })
    }

    // Actions ---------------------------------------------------------------------------------------------------------

    me.connect = function(uri) {
        me.socket = io.connect(uri)
        me.socket.on("connect", me.onConnected)
        me.socket.on("users", me.onUsersListMessage)
        me.socket.on("chat", me.onChatMessage)
        me.socket.on("stage", me.onStageMessage)
    }

    me.say = function(message) {
        me.socket.emit("chat", { msg: message });
    }

    // Private members -------------------------------------------------------------------------------------------------

    me._renderUsersList = function(users) {
        $("#run-users-list").empty()
        for (user of users) {
            $("#run-users-list").append("<li>" + user.name + "</li>")
        }
    }

    me._appendChatMessage = function(data) {
        $("#messages").append("<li>" + data["who"] + ": " + data["msg"] + "</li>")
    }

    me._renderStage = function(data) {
        data.stageType = function() { return data.stage.type; }

        var html = me.stageTemplate(data)
        $("#stage").html(html)

        if (data.stage.type == "voting") {
            $('.vote-details').popover({ trigger: "hover" })
        }
    }

    return me
}

$(document).ready(function() {
    var host = "http://" + document.domain + ":" + location.port
    var sessionKey = $("#session-key").text().trim()
    var controller = createSessionController(sessionKey)
    window.controller = controller

    controller.connect(host)

    $("#chat-message").keypress(function (e) {
        if (e.which == 13) {
            var msg = $("#chat-message").val()
            $("#chat-message").val("")
            controller.say(msg)
            return false;
        }
    })
})
