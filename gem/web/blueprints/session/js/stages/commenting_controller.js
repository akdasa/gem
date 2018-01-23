function CommentingStageController(session) {
    var commentsWidget = CommentsWidget({
        onFilterChanged: onCommentsWidgetFilterChanged
    })
    var commentQuote = null
    var state = null
    var comments = []
    var filterCheckedTypes = ["plus", "minus", "info"]
    var filterCheckedRoles = null
    var filterCheckedSort = ["timestamp"]

    function register() {
        $("#comment-private").on("change", onPrivateCommentsCheckboxChanged)
        $(".comment-add").on("click", onAddCommentButtonClicked)
        $("#proposal-content").on("mouseup", onProposalContentMouseUp)
        $(".selectpicker").selectpicker()
        commentsWidget.register()
    }

    function setState(value) {
        var isPresenter = session.user.permissions.contains("presenter")

        state = value
        commentsWidget.setComments(value.comments.list, {
            proposal_id: value.proposal_id,
            stage: value.comments.stage
        })
        commentsWidget.setPrivate(state.private)
        commentsWidget.setManageable(session.user.permissions.contains("comment.manage"))
        commentsWidget.setFilterVisibility(!isPresenter)
        commentsWidget.setPrintButtonVisibility(!isPresenter)
    }

    function view() {
        var permissions = session.user.permissions

        return Object.assign({}, state, {
            showComments: !state.private || permissions.indexOf("comment.manage") != -1,
            showAddComment: permissions.indexOf("comment") != -1,
            showAddCommentLink: permissions.indexOf("comment") != -1 && !state.private,
            comments: commentsWidget.view()
        })
    }

    function enter() {
        var timerValue = session.timers.get("commenting")
        controller.manage.setCountdownTimer(timerValue)
    }

    // UI Event handlers

    // "Secret ballot" checkbox clicked
    function onPrivateCommentsCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setCommentingPrivacy(val)
    }

    function onProposalContentMouseUp(e) {
        var selection = window.getSelection().toString()
        setCommentQuote(selection)
    }

    function onAddCommentButtonClicked(e) {
        e.preventDefault();
        var buttonClicked = $(this)
        var content = $("#comment-message").val()
        var type = $("#comment-type option:selected").val()
        comment(content, type, commentQuote)
    }

    function onCommentSubmittedResponse(data) {
        var flash = $("#comment-submitted")
        flash.removeClass("hidden")
        setTimeout(function() { flash.alert("close") }, 5000)
    }

    function onCommentsWidgetFilterChanged(filter) {
        session.stage.requestRender()
    }

    // Actions

    function comment(content, type, quote) {
        session.socket.emit("comment", {content, type, quote}, onCommentSubmittedResponse)
    }

    function setCommentingPrivacy(value) {
        session.socket.emit("manage", {private: value})
    }


    function setCommentQuote(value) {
        commentQuote = value
        $("#quotation").html(commentQuote)
        $("#quotation").attr("hidden", value ? null : "hidden")
    }

    return { register, view, setState, enter }
}
