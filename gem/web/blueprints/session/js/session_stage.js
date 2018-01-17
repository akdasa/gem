/* Stage Controller
 *
 * param session: Session
 * param proposalNode: Node to render proposal
 * param widgetsNode: Node to render stage widgets */
function StageController(session, proposalNode, widgetsNode) {

    // Process incoming message from server
    // param data: data from server
    function processMessage(data) {
        var proposalId = data.proposal_id
        var stageType = data.stage.type
        var nextStage = getController(proposalId, stageType) // controller for next stage
        var isStageChanged = (nextStage != currentStage)
        var isProposalChanged = (proposalId != (currentStage && currentStage.view().proposal_id))

        if (nextStage) {
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

            if (isStageChanged) {
                onStageChanged(currentStage, nextStage)
            }

            if (isProposalChanged) {
                onProposalChanged(nextStage.view().proposal)
            }
            currentStage = nextStage
        }

        // state is changes, so render it
        renderWidget()

        if (data.stage.type != "acquaintance") {
            $(".panel-body", proposalNode).addClass("proposal-block")
        } else {
            $(".panel-body", proposalNode).removeClass("proposal-block")
        }
    }

    function requestRender() {
        renderWidget()
    }

    // Private members

    // Renders current stage
    function renderWidget() {
        if (!currentStage) return;

        widgetsNode.html(widgetTemplate(currentStage.view()))
        if (currentStage.register) currentStage.register()
    }

    // Renders specified proposal
    function renderProposal(proposal) {
        var template = proposalTemplate(proposal)
        proposalNode.html(template)
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

    function onProposalChanged(proposal) {
        renderProposal(proposal)
    }

    // Private members

    var currentStage = null
    var proposalTemplate = Handlebars.compile($("#stage-proposal-template").html())
    var widgetTemplate = Handlebars.compile($("#stage-template").html())
    var proposals = JSON.parse($("#proposals").html())
    var controllers = {} // map of controllers keyed by proposalId

    // returns controllers for specified proposal
    // param proposalId: Id of proposal
    // param stage: Stage
    function getController(proposalId, stage) {
        var c = controllers[proposalId]
        if (!c) {
            c = createControllers()
            controllers[proposalId] = c
        }
        return c[stage]
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

    return { processMessage, requestRender }
}