function votingStageController(controller) {
    voteStatus = null;

    function register() {
        $("#vote-private").on("change", onSecretBallotCheckboxChanged)
        $(".vote").on("click", onVoteButtonClicked)
    }

    function view() {
        return {voteStatus: voteStatus}
    }

    function onSecretBallotCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setVotingPrivacy(val)
    }

    function onVoteButtonClicked(e) {
        e.preventDefault()
        var value = $(this).data("vote")
        vote(value)
    }

    function onVoteResponse(response) {
        voteStatus = response
        controller.render()
    }

    function setVotingPrivacy(value) {
        controller.socket.emit("manage", {private: value})
    }

    function vote(value) {
        controller.socket.emit("vote", {value: value}, onVoteResponse)
    }

    return { register, view }
}


function commentingStageController(controller) {
    var commentQuote = null

    function register() {
        $("#comment-private").on("change", onPrivateCommentsCheckboxChanged)
        $("#comment-filter input").on("change", onFilterCheckboxChanged)
        $(".comment-add").on("click", onAddCommentButtonClicked)
        $("#proposal-content").on("mouseup", onProposalContentMouseUp)
    }

    // UI Event handlers

    // "Secret ballot" checkbox clicked
    function onPrivateCommentsCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setCommentingPrivacy(val)
    }

    // on any filter checkbox changed
    function onFilterCheckboxChanged(e) {
        // get list of checked types and roles
        var checked_types = getCheckedFilterTypes()
        var checked_roles = getCheckedFilterRoles()

        // hide all comments and show filtered
        hideAllComments()
        showCommentsBy(function(idx, obj) {
            var role = $(obj).data("role")
            var name = $(obj).data("name")
            var type = $(obj).data("type")

            return checked_types.indexOf(type) >= 0 &&
                checked_roles.indexOf(role) >= 0
        })
    }

    function onProposalContentMouseUp(e) {
        var selection = window.getSelection().toString()
        setCommentQuote(selection)
    }

    function onAddCommentButtonClicked(e) {
        e.preventDefault();
        var buttonClicked = $(this)
        var content = $("#comment-message").val()
        var type = $(buttonClicked).data("type")
        comment(content, type, commentQuote)
    }

    // Actions

    function comment(content, type, quote) {
        controller.socket.emit("comment", {content, type, quote})
        console.log(content, type)
    }

    function setCommentingPrivacy(value) {
        controller.socket.emit("manage", {private: value})
    }

    function hideAllComments() {
        $('#comment-list>.media').hide()
    }

    function showCommentsBy(filter) {
        $('#comment-list>.media').filter(filter).show()
    }

    function setCommentQuote(value) {
        commentQuote = value
        $("#quotation").html(commentQuote)
        $("#quotation").attr("hidden", value ? null : "hidden")
    }

    function getCheckedFilterTypes() {
        return $("#comment-filter input.type:checked")
            .map(function(idx, obj) { return $(obj).val(); })
            .toArray();
    }

    function getCheckedFilterRoles() {
        return $("#comment-filter input.role:checked")
            .map(function(idx, obj) { return $(obj).val(); })
            .toArray();
    }

    return { register }
}

function discussionStageController(controller) {
    function register() {
        $(".discussion-give-voice").on("click", giveVoiceUserClicked)
        $("#discussion-raise-hand").on("click", raiseHandButtonClicked)
        $("#discussion-withdraw-hand").on("click", withdrawHandButtonClicked)
    }

    function giveVoiceUserClicked(e) {
        e.preventDefault();
        var userId = $(this).data("user-id")
        giveVoice(userId)
    }

    function raiseHandButtonClicked(e) {
        controller.socket.emit("manage", { command: "raise_hand" })
    }

    function withdrawHandButtonClicked(e) {
        controller.socket.emit("manage", { command: "withdraw_hand" })
    }

    function giveVoice(userId) {
        controller.socket.emit("manage", {command: "give_voice", user_id: userId})
    }

    return { register }
}
