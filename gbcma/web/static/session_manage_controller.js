function createRunManageController(sessionKey) {
    var me = {}

    me.sessionKey = sessionKey;

    me.onNextStageResponse = function(data) {
        console.log(data)
    }

    me.nextStage = function(step) {
        console.log("next stage")
        me.socket.emit("next", { session: me.sessionKey, step: step }, me.onNextStageResponse)
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
    var realTimeHost = 'http://' + document.domain + ':' + location.port;
    var sessionKey = $("#session-key").text().trim()
    var controller = createRunManageController(sessionKey)

    controller.connect(realTimeHost)

    $(".run-next").on("click", function(e) {
        e.preventDefault()
        var step = $(this).data("step")
        controller.nextStage(step)
     })
})