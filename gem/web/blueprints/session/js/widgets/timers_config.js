function TimersConfigWidget() {

    function register() {
        $("#session-set-timers").on("click", onSetTimerClicked)
    }

    function setup() {
        var view = dialogView({
            timers,
            value: function(name) { return timers[name].value }
        })

        alerts.dialog({
            title: "Set timers",
            view: view,
            action: onConfigSubmit
        })
    }

    function set(name, value) {
        timers[name] = value
    }

    function get(name) {
        return timers[name].value
    }

    var dialogView = Handlebars.compile("{{> timers_config }}")
    var alerts = Alerts()
    var timers = {
        voting:     { name: "Voting (min)", value: 1, def: 1 },
        commenting: { name: "Commenting (min)", value: 2, def: 2 },
        discussion: { name: "Discussion (min)", value: 3, def: 3 }
    }

    function onSetTimerClicked() {
        setup()
    }

    function onConfigSubmit(dlg) {
        for (timer in timers) {
            var val = dlg.$content.find("#" + timer).val()
            timers[timer].value = Number(val) || timers[timer].def
        }
    }

    return { get, set, setup, register }
}