function createManageController(controller) {
    var nextStageLabel = $("#state-next")


    $(".change-stage").on("click", function(e) {
        e.preventDefault()
        var value = $(this).data("value")
        changeStage(value)
    })

    $(".run-close").on("click", function(e) {
        e.preventDefault()
        closeSession()
    })

    $("#stage").on("click", ".run-close", function(e) {
        e.preventDefault()
        closeSession()
    })

    $(".timer-set").on("click", function(e) {
        e.preventDefault()
        var minutes = $(this).data("value")
        if (minutes == "custom") {
            minutes = prompt("Time in minutes. (Start with the '+' sign to add time to the current timer)", "1")
        }
        setCountdownTimer(minutes)
    })


    function onChangeStageResponse(data) {
        if (data.next.title != data.current.title) {
            var title = data.next.title ? " &laquo;" + data.next.title + "&raquo;" : ""
            nextStageLabel.html(title)
        } else {
            var type = data.next.type ? " (" + data.next.type + ")" : ""
            nextStageLabel.html(type)
        }
    }

    // Actions ---------------------------------------------------------------------------------------------------------

    function changeStage(value) {
        controller.socket.emit("change_stage", { value: value }, onChangeStageResponse)
    }

    function closeSession() {
        controller.socket.emit("close", onCloseSessionResponse)
    }

    function setCountdownTimer(minutes) {
        controller.socket.emit("timer", { interval: minutes })
    }


    return {}
}
