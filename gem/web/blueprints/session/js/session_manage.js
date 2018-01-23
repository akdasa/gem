function createManageController(controller) {
    var nextStageLabel = $("#state-next")
    var alerts = Alerts()


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
            minutes = promptCustomTimer()
        } else {
            setCountdownTimer(minutes)
        }
    })

    $("#session-quorum-set").on("click", function(e) {
        e.preventDefault()
        controller.quorum.requestChange()
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

    function onCloseSessionResponse(data) {
        alerts.alert({title: "Closed", message: "Session is closed. You will be redirected to the dashboard page."}, function () {
            window.location = "/"
        })
    }

    // Actions ---------------------------------------------------------------------------------------------------------

    function changeStage(value) {
        controller.socket.emit("change_stage", { value: value }, onChangeStageResponse)
    }

    function closeSession() {
        controller.socket.emit("close", onCloseSessionResponse)
    }

    function setCountdownTimer(minutes) {
        if (controller.user.permissions.contains("session.manage")) {
            controller.socket.emit("timer", { interval: minutes })
        }
    }

    function promptCustomTimer() {
        $.confirm({
            theme: "bootstrap",
            title: 'Custom timer',
            content: $("#timer-custom").html(),
            buttons: {
                formSubmit: {
                    text: 'Submit',
                    btnClass: 'btn btn-primary',
                    action: function () {
                        var value = this.$content.find('#timer-custom-value').val()
                        if (!value) {
                            $.alert('Provide a valid value')
                            return false
                        }
                        setCountdownTimer(value)
                    }
                },
                cancel: {
                    btnClass: "btn btn-danger",
                    text: "Cancel",
                    action: function () {}
                }
            },
            onContentReady: function () {
                // bind to events
                var jc = this;
                this.$content.find('form').on('submit', function (e) {
                    // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click'); // reference the button and click it
                })
            }
        })
    }


    return { setCountdownTimer }
}
