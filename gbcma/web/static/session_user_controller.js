function extendSessionController(me) {

    // Handlers --------------------------------------------------------------------------------------------------------

    me.onVoteResponse = function(data) {
        console.log(data)
    }

    // Actions ---------------------------------------------------------------------------------------------------------

    me.vote = function(value) {
        me.socket.emit("vote", {value: value}, me.onVoteResponse)
    }

    return me
}

$(document).ready(function() {
    extendSessionController(controller)

    $("body").on("click", ".vote", function(e) {
        e.preventDefault();
        var value = $(this).data("vote")
        controller.vote(value)
    })
})