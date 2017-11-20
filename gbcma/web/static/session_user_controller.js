function extendSessionController(me) {

    me.quotation = null

    // Handlers --------------------------------------------------------------------------------------------------------

    me.onVoteResponse = function(data) {
        console.log(data)
    }

    me.onCommentResponse = function(data) {
        console.log(data)
    }

    // Actions ---------------------------------------------------------------------------------------------------------

    me.vote = function(value) {
        me.socket.emit("vote", {value: value}, me.onVoteResponse)
    }

    me.comment = function(content, type, quote) {
        me.socket.emit("comment", {content: content, type: type, quote: quote}, me.onCommentResponse)
        console.log(content, type)
    }

    me.raiseHand = function() {
        me.socket.emit("raise_hand", {})
    }

    me.withdrawHand = function() {
        me.socket.emit("withdraw_hand", {})
    }

    me.setQuotation = function(value) {
        me.quotation = value
        $("#quotation").html(me.quotation)
        $("#quotation").attr("hidden", null)
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

    $("body").on("click", ".comment-add", function(e) {
        e.preventDefault();
        var content = $("#comment-message").val()
        var type = $(this).data("type")
        controller.comment(content, type, controller.quotation)
    })

    $("body").on("mouseup", "#proposal-content", function() {
        var quote = window.getSelection().toString()
        controller.setQuotation(quote)
    })

    $("body").on("click", "#discussion-raise-hand", function(e) {
        e.preventDefault()
        controller.raiseHand()
    })

    $("body").on("click", "#discussion-withdraw-hand", function(e) {
        e.preventDefault()
        controller.withdrawHand()
    })
})