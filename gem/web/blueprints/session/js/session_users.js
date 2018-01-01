/* Manages the list of connected users. */
function createUsersController(controller) {

    $(document).on("click", ".kick", onKickButtonClicked)

    // Processes incoming message
    // param: data - array of connected users
    //        [{name: "akd", role: "secretary"}, ...]
    function processMessage(data) {
        users = data
        render()
    }

    // Private members

    var users    = []
    var panel    = $("#session-users-list")
    var line     = $("#session-users-line").html()
    var template = Handlebars.compile(line)


    function onKickButtonClicked() {
        var userId = $(this).data("user-id")
        showKickDialog(function (reason) {
            controller.socket.emit("kick", {user: userId, reason})
        })
    }

    function showKickDialog(callback) {
        $.confirm({
            title: 'Kick!',
            type: 'red',
            content: '' +
            '<form action="" class="form">' +
            '<div class="form-group">' +
            '<textarea placeholder="Reason" class="reason form-control" ></textarea>' +
            '</div>' +
            '</form>',
            buttons: {
                formSubmit: {
                    text: 'Kick',
                    btnClass: 'btn-danger',
                    action: function () {
                        var reason = this.$content.find('.reason').val();
                        callback(reason)
                    }
                },
                cancel: function () {
                    //close
                },
            },
            onContentReady: function () {
                // bind to events
                var jc = this;
                this.$content.find('form').on('submit', function (e) {
                    // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click'); // reference the button and click it
                });
            }
        })
    }

    function render() {
        panel.empty()
        for (user of users) {
            panel.append(template(user, {data: {user: controller.user}}))
        }
    }

    return { processMessage, render }
}
