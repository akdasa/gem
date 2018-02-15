/* Manages the timer. */
function createTimerController(controller) {

    function processMessage(data) {
        var minutes = data.interval

        if (!minutes) {
            stop()
            return
        }

        var isAppendMode = minutes.toString().indexOf("+") != -1
        if (isAppendMode) { // append to current time
            if (end == null) end = new Date().getTime()
            end += minutes * 60000
        } else { // set new time
            end = new Date().getTime() + (minutes * 60000)
        }
        countdownTo(new Date(end))
    }

    function countdownTo(date) {
        // timer was started previously.
        // stop it before start new one
        if (timer) {
            clearInterval(timer)
        }

        // sets new timer
        end = date.getTime()
        timer = setInterval(render, 1000)

        showPanel(true)
        render()
    }

    function stop() {
        end = null
        if (timer) {
            clearInterval(timer)
        }
        showPanel(false)
    }

    function on(handler) {
        callbacks.push(handler)
    }

    function off(handler) {
        callbacks.remove(handler)
    }

    // Private members

    var timer = null  // timer object
    var end   = null  // countdown to this date/time
    var panel = $("#timer-panel") // timer's panel
    var callbacks = []

    // Shows timer's panel
    // param: value  - true/false
    // param: danger - true/false, highlight panel or not
    function showPanel(value, danger) {
        panel.toggle(value)
        if (danger) {
            panel.addClass("panel-danger")
        } else {
            panel.removeClass("panel-danger")
        }
    }
    function showPanel1(value, danger) {
        panel.toggle(value)
        if (danger) {
            panel.addClass("panel-warning")
        } else {
            panel.removeClass("panel-warning")
        }
    }

    // Renders panel
    function render() {
        var now = new Date().getTime()
        var distance = end - now
        for (c in callbacks) {
            callbacks[c](distance)
        }
        var diff = timeDiff(now, end);

        if (distance < 0) {
	        showPanel(true, true)
        }

        if (diff.negative) {
            document.getElementById("timer").innerHTML = "- " + diff.minutes + ":" + diff.seconds;
        } else {
            document.getElementById("timer").innerHTML = diff.minutes + ":" + diff.seconds;
        }

        if (distance < 1000 * 30) {
            showPanel1(true, true)
        }
    }

    return { processMessage, countdownTo, stop, on, off }
}
