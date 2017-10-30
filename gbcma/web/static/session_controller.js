function createRunController(sessionKey) {
    var me = {}

    me.sessionKey = sessionKey;
    me.stageTemplate = Handlebars.compile($("#stage-template").html())

    me.onConnected = function(socket) {
        me.socket.emit("join", { room: me.sessionKey })
    }

    me.onUsersListMessage = function(data) {
        console.log("users", data)
        me._renderUsersList(data)
    }

    me.onChatMessage = function(data) {
        me._appendChatMessage(data)
    }

    me.onStageMessage = function(data) {
        console.log(data)
        me._renderStage(data)
    }

    me.connect = function(uri) {
        me.socket = io.connect(uri)
        me.socket.on("connect", me.onConnected)
        me.socket.on("users", me.onUsersListMessage)
        me.socket.on("chat", me.onChatMessage)
        me.socket.on("stage", me.onStageMessage)
        console.log(uri)
    }

    me.say = function(message) {
        me.socket.emit("chat", { msg: message });
    }

    me._renderUsersList = function(users) {
        $("#run-users-list").empty();

        for (user of users) {
            $("#run-users-list").append("<li>" + user.name + "</li>");
            //console.log("users: ", user);
        }
    }

    me._appendChatMessage = function(data) {
        $("#messages").append("<li>" + data["who"] + ": " + data["msg"] + "</li>");
    }

    me._renderStage = function(data) {
        console.log(data)
        var html = me.stageTemplate(data)
        $("#stage").html(html)
    }


    return me
}

$(document).ready(function() {
    var realTimeHost = 'http://' + document.domain + ':' + location.port;
    var sessionKey = $("#session-key").text().trim()

    var controller = createRunController(sessionKey)
    controller.connect(realTimeHost)

    $('#chat-message').keypress(function (e) {
        if (e.which == 13) {
            var msg = $("#chat-message").val();
            controller.say(msg);
            return false;    //<---- Add this line
        }
     });
})