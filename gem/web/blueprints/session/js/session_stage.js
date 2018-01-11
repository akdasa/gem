/* Stage Controller
 *
 * param session: Session
 * param node: Node to render session view
 */
function StageController(session, node) {

    function processMessage(data) {
        var proposalId = data.proposal_id
        var type = data.stage.type
        var nextStage = getControllers(proposalId)[type] // controller for next stage
        var isStageChanged = (nextStage != currentStage)

        if (isStageChanged) {
            onStageChanged(currentStage, nextStage)
        }

        if (nextStage) {
            currentStage = nextStage

            // extend data with additional info
            Object.assign(data, {
                stageType: function() { return data.stage.type },
                proposal: data.proposal_id ? proposals[data.proposal_id] : null,
                user: session.user
            })

            // updates state of the stage controller
            if (nextStage.setState) {
                nextStage.setState(data)
            }
        }

        // state is changes, so render it
        render()
    }

    // renders current stage
    function render() {
        if (!currentStage) return;

        // render and register handlers
        node.html(template(currentStage.view()))
        if (currentStage.register) currentStage.register()
    }

    // Event handlers

    function onStageChanged(current, next) {
        // stage changed - stop the timer
        session.timer.stop()

        // unregister handlers from current stage
        if (current && current.unregister) {
            currentStage.unregister()
        }

        // call "enter" handler for next stage
        if (next && next.enter) {
            nextStage.enter()
        }
    }

    // Private members

    var currentStage = null
    var template = Handlebars.compile($("#stage-template").html())
    var proposals = JSON.parse($("#proposals").html())
    var controllers = {} // map of controllers keyed by proposalId

    // returns controllers for specified proposal
    // param proposalId: Id of proposal
    function getControllers(proposalId) {
        var c = controllers[proposalId]
        if (!c) {
            c = createControllers()
            controllers[proposalId] = c
        }
        return c
    }

    // creates a bunch of controllers for each stage
    function createControllers() {
        return {
            "agenda": SimpleStageController(session),
            "acquaintance": SimpleStageController(session),
            "closed": SimpleStageController(session),
            "voting": VotingStageController(session),
            "votingresults": VotingResultsStageController(session),
            "commenting": CommentingStageController(session),
            "discussion": DiscussionStageController(session)
        }
    }

    return { processMessage, render }
}