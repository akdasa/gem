/* Module for creating pop-up notifications */

function Alerts() {

    function red_alert(title, message, action) {
        $.alert({
            title: title,
            content: message,
            type: "red",
            buttons: {
                confirm: {
                    text: "Ok",
                    action: action
                }
            }
        })
    }

    function input(title, message, action) {
        $.confirm({
            title: title,
            type: "red",
            content: '' +
            '<form action="" class="form">' +
            '<div class="form-group">' +
            '<textarea placeholder="'+message+'" class="form-control" id="msg"></textarea>' +
            '</div>' +
            '</form>',
            buttons: {
                formSubmit: {
                    text: "Ok",
                    btnClass: "btn-danger",
                    action: function () {
                        var msg = this.$content.find("#msg").val();
                        action(msg)
                    }
                },
                cancel: function () {}
            }
        })
    }

    return {alert:red_alert, input}
}