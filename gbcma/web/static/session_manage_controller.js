function createRunManageController(sessionKey) {
    var me = {}

    me.sessionKey = sessionKey;

    me.onNextStageResponse = function(data) {
        console.log(data)
    }

    me.onCloseSessionResponse = function(data) {
        console.log(data)
    }

    me.nextStage = function(step) {
        me.socket.emit("next", { session: me.sessionKey, step: step }, me.onNextStageResponse)
    }

    me.closeSession = function() {
        me.socket.emit("close", me.onCloseSessionResponse)
    }

    me.connect = function(uri) {
        me.socket = io.connect(uri)
        me.socket.on("connect", me.onConnected)
        console.log(uri)
    }

    me.onConnected = function(socket) {
        me.socket.emit("join", { room: me.sessionKey })
    }

    return me
}

$(document).ready(function() {
    var realTimeHost = "http://" + document.domain + ":" + location.port;
    var sessionKey = $("#session-key").text().trim()
    var controller = createRunManageController(sessionKey)

    controller.connect(realTimeHost)

    $(".run-next").on("click", function(e) {
        e.preventDefault()
        var step = $(this).data("step")
        controller.nextStage(step)
    })

    $(".run-close").on("click", function(e) {
        e.preventDefault()
        controller.closeSession()
    })

    $("#stage").on("click", ".run-close", function(e) {
        e.preventDefault()
        controller.closeSession()
    })
})
