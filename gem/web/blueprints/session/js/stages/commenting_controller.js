function CommentingStageController(session) {
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
        $("#comment-filter-type").on("changed.bs.select", onFilterChanged)
        $("#comment-filter-role").on("changed.bs.select", onFilterChanged)
        $("#comment-sort").on("changed.bs.select", onFilterChanged)

        $("#comment-print").on("click", onPrintClicked)
    }

    function setState(value) {
        state = value

        comments = state.comments.list
        roles = state.comments.list.map(function(obj) { return obj.role })
        roles = roles.filter(function(v, i) { return roles.indexOf(v) == i })
        filterCheckedRoles = roles
        updateComments()
    }

    function view() {
        var permissions = session.user.permissions

        return Object.assign({}, state, {
            showComments: !state.private || permissions.indexOf("comment.manage") != -1,
            showAddComment: permissions.indexOf("comment") != -1,
            showAddCommentLink: permissions.indexOf("comment") != -1 && !state.private,
            comments: {
                showFilter: true,
                showPrint: true,
                manageable: permissions.indexOf("comment.manage") != -1,
                privateCheckedState: state.private ? "checked" : "",
                comments: comments,
                roles: roles,
                filterTypeValue: function(name) { return filterCheckedTypes.indexOf(name) != -1 ? "selected" : "" },
                filterRoleValue: function(name) { return filterCheckedRoles.indexOf(name) != -1 ? "selected" : "" },
                filterSortValue: function(name) { return filterCheckedSort.indexOf(name) != -1 ? "selected" : "" }
            }
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
        filterCheckedTypes = $("#comment-filter-type").val()
        filterCheckedRoles = $("#comment-filter-role").val()
        filterCheckedSort = $("#comment-sort").val()
        updateComments()
        session.stage.requestRender()
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

    function onPrintClicked(e) {
        e.preventDefault()

        var alert = Alerts().alert({
            title:"Printing",
            message:"We are printing your document. Please wait a moment."
        })

        var commentsCriteria = { proposal_id: state.proposal_id, stage: state.comments.stage }
        var data = {type:"comments", "criteria": commentsCriteria}

        controller.emit("print", data, function(data) {
            if (data.success) {
                $.fileDownload("/files/" + data.path)
                alert.close()
            } else {
                Alerts().alert({title: "Error", message: data.message})
            }
        })
    }

    // Actions

    function comment(content, type, quote) {
        session.socket.emit("comment", {content, type, quote}, onCommentSubmittedResponse)
    }

    function setCommentingPrivacy(value) {
        session.socket.emit("manage", {private: value})
    }

    function updateComments() {
        showComments(function(x) {
            return filterCheckedTypes.indexOf(x.type) >= 0 &&
                filterCheckedRoles.indexOf(x.role) >= 0
        }, function (a, b) {
            if (filterCheckedSort != "time") {
                var fa = a[filterCheckedSort]
                var fb = b[filterCheckedSort]
                return fa !== fb ? fa < fb ? -1 : 1 : 0
            } else {
                var fa = Date.parse(a[filterCheckedSort])
                var fb = Date.parse(b[filterCheckedSort])
                return fa !== fb ? fa < fb ? -1 : 1 : 0
            }
        })
    }

    function showComments(func, sort) {
        for (c of comments) {
            c.visible = func(c)
        }
        if (sort) {
            comments = comments.sort(sort)
        }
    }

    function setCommentQuote(value) {
        commentQuote = value
        $("#quotation").html(commentQuote)
        $("#quotation").attr("hidden", value ? null : "hidden")
    }

    return { register, view, setState }
}
