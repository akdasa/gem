/* Acquaintance stage controller
 * Provides basic functionality
 * param session: session
 */
function AcquaintanceStageController(session) {

    function setState(value) {
        var isPresenter = session.user.permissions.contains("presenter")
        var isDeputiesReviewStage = value.proposal.state == "deputies_review"

        state = value

        commentsWidget.setComments(value.comments.list, {
            proposal_id: value.proposal_id,
            stage: value.comments.stage
        })
        votingResultsWidgets.setResults(state.voting)

        var showDetailWidgets = !(isPresenter || isDeputiesReviewStage)
        votingResultsWidgets.setVisibility(showDetailWidgets)
        commentsWidget.setVisibility(showDetailWidgets)
        commentsWidget.setFilterVisibility(!isPresenter)
        commentsWidget.setPrintButtonVisibility(!isPresenter)
        commentsWidget.getPrintCommentsWidget().setOptions({
            anonymous: value.comments.stage == "deputies_review"
        })
    }

    function register() {
        $(".selectpicker").selectpicker()
        $(".vote-details").popover({ trigger: "hover" })
        commentsWidget.register()
    }

    function view() {
        return {
            comments: commentsWidget.view(),
            voting: votingResultsWidgets.view(),
            stageType: state.stageType,
            proposal_id: state.proposal_id
        }
    }

    // Private members

    var state = null
    var commentsWidget = CommentsWidget({
        onFilterChanged: onCommentsWidgetFilterChanged
    })
    var votingResultsWidgets = VotingResultsWidget()

    function onCommentsWidgetFilterChanged(filter) {
        session.stage.requestRender()
    }

    return { view, setState, register }
}
