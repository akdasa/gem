/* Module for creating pop-up notifications */

function Alerts() {

    function red_alert(options, action) {
        return $.alert({
            title: options.title || "Alert",
            content: options.message || "",
            type: "red",
            buttons: {
                confirm: {
                    text: "Ok",
                    action: action || function() {}
                }
            }
        })
    }

    function input(options, action) {
        // title, message, placeholder, action
        return $.confirm({
            title: options.title,
            type: "red",
            content: (options.message || "") +
            '<form action="" class="form">' +
            '<div class="form-group">' +
            '<textarea placeholder="'+(options.placeholder||"")+'" class="form-control" id="msg"></textarea>' +
            '</div>' +
            '</form>',
            buttons: {
                formSubmit: {
                    text: "Ok",
                    btnClass: "btn-danger",
                    action: function () {
                        var msg = this.$content.find("#msg").val();
                        if (action) {
                            if (options.data)
                                action(msg, options.data)
                            else
                                action(msg)
                        }
                    }
                },
                cancel: function () {}
            }
        })
    }

    function dialog(options) {
        return $.confirm({
            title: options.title,
            type: "red",
            content: options.view,
            columnClass: "s",
            buttons: {
                formSubmit: {
                    text: "Ok",
                    btnClass: "btn-danger",
                    action: function () {
                        if (options.action) options.action(this)
                    }
                },
                cancel: function () {}
            }
        })
    }

    return { alert:red_alert, input, dialog }
}