function extendSessionController(me) {
    me.onChangeStageResponse = function(data) {
        //console.log(data)
    }

    me.onCloseSessionResponse = function(data) {
        //console.log(data)
    }


    // Actions ---------------------------------------------------------------------------------------------------------

    me.changeStage = function(value) {
        me.socket.emit("change_stage", { value: value }, me.onChangeStageResponse)
    }

    me.closeSession = function() {
        me.socket.emit("close", me.onCloseSessionResponse)
    }

    return me
}

$(document).ready(function() {
    extendSessionController(controller)

    $(".change-stage").on("click", function(e) {
        e.preventDefault()
        var value = $(this).data("value")
        controller.changeStage(value)
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
