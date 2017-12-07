function createSessionController(sessionKey) {
    var me = {
        sessionKey: sessionKey,
        stageTemplate: Handlebars.compile($("#stage-template").html()),
        user: {},
        countdownTimer: null
    }

    // Handlers --------------------------------------------------------------------------------------------------------

    me.onTimerMessage = function(data) {
        var minutes = data.interval
        var to = new Date().getTime() + (minutes * 60000)
        me.countdownTo(new Date(to))
    }

    me.onUserInfoMessage = function(data) {
        me.user = data
    }

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
        me.socket.on("user", me.onUserInfoMessage)
        me.socket.on("timer", me.onTimerMessage)
    }

    me.say = function(message) {
        me.socket.emit("chat", { msg: message });
    }

    me.countdownTo = function(date) {
        if (me.countdownTimer) {
            clearInterval(me.countdownTimer);
        }

        me.countdownTimer = setInterval(function() {
            var now = new Date().getTime();
            var distance = date - now;

            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Display the result in the element with id="demo"
            document.getElementById("timer").innerHTML =
                hours ? hours + "h " + minutes + ":" + seconds :
                        minutes + ":" + seconds;

            // If the count down is finished, write some text
            if (distance < 0) {
                clearInterval(me.countdownTimer);
                document.getElementById("timer").innerHTML = "EXPIRED";
            }
        }, 1000);
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
        data.stageType = function() { return data.stage.type }
        data.user = me.user

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

    Handlebars.registerPartial('agenda', $("#stage-agenda").html())
    Handlebars.registerPartial('acquaintance', $("#stage-acquaintance").html())
    Handlebars.registerPartial('voting', $("#stage-voting").html())
    Handlebars.registerPartial('commenting', $("#stage-commenting").html())
    Handlebars.registerPartial('discussion', $("#stage-discussion").html())
    Handlebars.registerPartial('closed', $("#stage-closed").html())
})
