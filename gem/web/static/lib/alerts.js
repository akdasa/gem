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

    return {alert:red_alert}
}