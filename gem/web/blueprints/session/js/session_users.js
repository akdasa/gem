/* Manages the list of connected users. */
function createUsersController(controller) {

    $(document).on("click", ".kick", onKickButtonClicked)

    // Processes incoming message
    // param: data - array of connected users
    //        [{name: "akd", role: "secretary"}, ...]
    function processMessage(data) {
        render(data)
    }

    // Private members

    var panel    = $("#session-users-list")
    var line     = "<li>{{name}} <small>{{role}}</small><a href='#'><span class='glyphicon glyphicon-remove kick' data-user-id='{{id}}'></span></a></li>"
    var template = Handlebars.compile(line)


    function onKickButtonClicked() {
        var userId = $(this).data("user-id")
        showKickDialog(function (reason) {
            controller.socket.emit("kick", {user: userId, reason})
        })
        //console.log(userId)
        //controller.socket.emit("kick", {user: userId})
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

    function render(users) {
        panel.empty()
        for (user of users) {
            panel.append(template(user))
        }
    }

    return { processMessage }
}
