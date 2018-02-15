function CommentsWidget(options) {

    function setComments(value, source) {
        comments = value

        summaryWidget.setComments(value)
        printDocumentWidget.setType("comments")
        printDocumentWidget.setArgs(source)

        possibleRoles = extractRolesFromComments(comments)
        filterWidget.setRoles(possibleRoles)
        if (lastFilter)
            updateComments(lastFilter)
    }

    function setManageable(value) {
        manageable = value
    }

    function setPrivate(value) {
        private = value
    }

    function setVisibility(value) {
        showWidget = value
    }

    function setFilterVisibility(value) {
        showFilter = value
    }

    function setPrintButtonVisibility(value) {
        showPrint = value
    }

    function getPrintCommentsWidget() {
        return printDocumentWidget
    }

    function view() {
        return {
            filter: filterWidget.view(),
            print: printDocumentWidget.view(),
            summary: summaryWidget.view(),
            showFilter, showPrint, manageable, comments, showWidget,
            privateCheckedState: private ? "checked" : ""
        }
    }

    function register() {
        filterWidget.register()
        printDocumentWidget.register()
    }

    // Private members

    var summaryWidget = CommentsSummaryWidget()
    var printDocumentWidget = PrintDocumentWidget()
    var filterWidget = CommentsFilterWidget({
        onFilterChanged: onFilterChanged
    })

    var comments = []
    var showFilter = true
    var showPrint = true
    var manageable = false
    var private = true
    var lastFilter = null
    var possibleRoles = []
    var showWidget = true


    // Returns list of unique roles present in comments
    // param comments: list of comments to extract roles from
    function extractRolesFromComments(comments) {
        var roles = comments.map(function(obj) { return obj.role })
        return roles.filter(function(v, i) { return roles.indexOf(v) == i && v != null})
    }

    function onFilterChanged(filter) {
        lastFilter = filter
        updateComments(filter)
        if (options.onFilterChanged) {
            options.onFilterChanged(filter)
        }
    }

    function updateComments(filter) {
        showComments(function(x) {
            return filter.types.contains(x.type) && (filter.roles.contains(x.role) || possibleRoles.length <= 0)
        })

        sortComments(function (a, b) {
            if (filter.sort != "time") {
                var fa = a[filter.sort]
                var fb = b[filter.sort]
                return fa !== fb ? fa < fb ? -1 : 1 : 0
            } else {
                var fa = Date.parse(a[filter.sort])
                var fb = Date.parse(b[filter.sort])
                return fa !== fb ? fa < fb ? -1 : 1 : 0
            }
        })
    }

    function showComments(func) {
        for (c of comments) {
            c.visible = func(c)
        }
    }

    function sortComments(func) {
        comments = comments.sort(func)
    }

    return {
        view, setComments, setPrivate, setManageable, setFilterVisibility,
        setPrintButtonVisibility, register, setVisibility, getPrintCommentsWidget
    }
}