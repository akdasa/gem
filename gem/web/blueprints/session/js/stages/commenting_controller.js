function CommentingStageController(session) {
    var commentQuote = null
    var state = null

    function register() {
        $("#comment-private").on("change", onPrivateCommentsCheckboxChanged)
        $(".comment-add").on("click", onAddCommentButtonClicked)
        $("#proposal-content").on("mouseup", onProposalContentMouseUp)

        $(".selectpicker").selectpicker()
        $("#comment-filter-type").on("changed.bs.select", onFilterChanged)
        $("#comment-filter-role").on("changed.bs.select", onFilterChanged)
    }

    function setState(value) {
        state = value
    }

    function view() {
        var permissions = session.user.permissions

        return Object.assign(state, {
            manageable: permissions.indexOf("comment.manage") != -1,
            privateCheckedState: state.private ? "checked" : "",
            showComments: !state.private || permissions.indexOf("comment.manage") != -1,
            showAddComment: permissions.indexOf("comment") != -1,
            showAddCommentLink: permissions.indexOf("comment") != -1 && !state.private
            showFilter: true,
        })
    }

    // UI Event handlers

    // "Secret ballot" checkbox clicked
    function onPrivateCommentsCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setCommentingPrivacy(val)
    }

    // on any filter checkbox changed
    function onFilterChanged(e) {
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
        var type = $("#comment-type option:selected").val()
        comment(content, type, commentQuote)
    }

    function onCommentSubmittedResponse(data) {
        var flash = $("#comment-submitted")
        flash.removeClass("hidden")
        setTimeout(function() { flash.alert("close") }, 5000)
    }

    // Actions

    function comment(content, type, quote) {
        session.socket.emit("comment", {content, type, quote}, onCommentSubmittedResponse)
    }

    function setCommentingPrivacy(value) {
        session.socket.emit("manage", {private: value})
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
        return $("#comment-filter-type").val()
    }

    function getCheckedFilterRoles() {
        return $("#comment-filter-role").val()
    }

    return { register, view, setState }
}
