/* Acquaintance stage controller
 * Provides basic functionality
 * param session: session
 */
function AcquaintanceStageController(session) {

    function setState(value) {
        state = value

        commentsWidget.setComments(value.comments.list, {
            proposal_id: value.proposal_id,
            stage: value.comments.stage
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

            voting: state.voting,
            stageType: state.stageType,
            proposal_id: state.proposal_id
        }
    }

    // Private members

    var state = null
    var commentsWidget = CommentsWidget({
        onFilterChanged: onCommentsWidgetFilterChanged
    })

    function onCommentsWidgetFilterChanged(filter) {
        session.stage.requestRender()
    }

    return { view, setState, register }
}
