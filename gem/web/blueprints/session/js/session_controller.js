// Session controller

function createSessionController(sessionKey) {
    var me = {
        sessionKey: sessionKey,
        stageTemplate: Handlebars.compile($("#stage-template").html()),
        user: {},
        countdownTimer: null,
        timerPanel: $("#timer-panel"),
        lastStageType: null,
        proposals: JSON.parse($("#proposals").html()),
        stages: {},
        timerEnd: null
    }

    me.stages["voting"] = votingStageController(me)
    me.stages["commenting"] = commentingStageController(me)
    me.stages["discussion"] = discussionStageController(me)

    // Handlers --------------------------------------------------------------------------------------------------------

    me.onTimerMessage = function(data) {
        console.log(data)
        var minutes = data.interval
        if (minutes) {
            var isAppendMode = minutes.toString().indexOf("+") != -1
            if (isAppendMode) {
                if (me.timerEnd == null) me.timerEnd = new Date().getTime()
                me.timerEnd += minutes * 60000
            } else {
                me.timerEnd = new Date().getTime() + (minutes * 60000)
            }
            me.countdownTo(new Date(me.timerEnd))
        } else {
            me.stopTimer()
            me._showTimerPanel(false)
        }
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
        // stage changed. Lets stop timer
        if (data.stage.type != me.lastStageType) {
            me.stopTimer()
            me._showTimerPanel(false)
        }

        //
        var stageController = me.stages[data.stage.type]
        if (stageController) {
            stageController.data = data
            if (stageController.enter) { stageController.enter() }
        }

        me.lastStageType = data.stage.type
        me._renderStage(data)

        if (stageController) {
            if (stageController.register) { stageController.register() }
        }
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
            clearInterval(me.countdownTimer)
        }

        me.countdownTimer = setInterval(function() {
            me._renderTimer(date)
        }, 1000)

        me._showTimerPanel(true)
        me._renderTimer(date)
    }

    me.stopTimer = function() {
        me.timerEnd = null
        if (me.countdownTimer) {
            clearInterval(me.countdownTimer)
        }
    }

    me.render = function(view) {
        var stageController = me.stages[me.lastStageType]
        if (stageController) {
            var view = stageController.view ? stageController.view() : {}
            me._renderStage(Object.assign({}, stageController.data, view))
            if (stageController.register) { stageController.register() }
        }
    }

    // Private members -------------------------------------------------------------------------------------------------

    me._renderUsersList = function(users) {
        $("#run-users-list").empty()
        for (user of users) {
            $("#run-users-list").append("<li>" + user.name + " <small>"+user.role+"</small></li>")
        }
    }

    me._appendChatMessage = function(data) {
        $("#messages").append("<li>" + data["who"] + ": " + data["msg"] + "</li>")
    }

    me._renderStage = function(data) {
        // provide some additional data for template
        data.stageType = function() { return data.stage.type }
        data.user = me.user

        // load cached proposal data if proposal id is provided
        if (data.proposal_id) {
            data.proposal = me.proposals[data.proposal_id]
        }

        // render template and apply to DOM
        var html = me.stageTemplate(data)
        $("#stage").html(html)

        // some dynamic
        // TODO: extract to somewhere else
        if (data.stage.type == "votingresults") {
            $('.vote-details').popover({ trigger: "hover" })
        }
    }

    me._showTimerPanel = function(value, danger) {
        me.timerPanel.toggle(value)
        if (danger) {
            me.timerPanel.addClass("panel-danger")
        } else {
            me.timerPanel.removeClass("panel-danger")
        }
    }

    me._renderTimer = function(date) {
        var now = new Date().getTime()
        var distance = date - now

        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        var seconds = Math.floor((distance % (1000 * 60)) / 1000)

        minutes = String("00" + minutes).slice(-2)
        seconds = String("00" + seconds).slice(-2)


        // Display the result in the element with id="demo"
        document.getElementById("timer").innerHTML =
            hours ? hours + "h " + minutes + ":" + seconds :
                    minutes + ":" + seconds

        if (distance < 0) {
            clearInterval(me.countdownTimer)
            document.getElementById("timer").innerHTML = "00:00"
        }

        if (distance < 1000 * 45) {
            me._showTimerPanel(true, true)
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
    Handlebars.registerPartial('votingresults', $("#stage-voting_results").html())
    Handlebars.registerPartial('commenting', $("#stage-commenting").html())
    Handlebars.registerPartial('discussion', $("#stage-discussion").html())
    Handlebars.registerPartial('closed', $("#stage-closed").html())
})
