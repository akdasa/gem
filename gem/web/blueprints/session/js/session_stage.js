/* Stage Controller
 *
 * param session: Session
 * param proposalNode: Node to render proposal
 * param widgetsNode: Node to render session stage widgets */
function StageController(session, proposalNode, widgetsNode) {

    function processMessage(data) {
        var proposalId = data.proposal_id
        var type = data.stage.type
        var nextStage = getControllers(proposalId)[type] // controller for next stage
        var isStageChanged = (nextStage != currentStage)
        var isProposalChanged = (data.proposal_id != (currentStage && currentStage.view().proposal_id))

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
        render()

        if (data.stage.type != "acquaintance") {
            $(".panel-body", proposalNode).addClass("proposal-block")
        } else {
            $(".panel-body", proposalNode).removeClass("proposal-block")
        }
    }

    // renders current stage
    function render() {
        if (!currentStage) return;

        widgetsNode.html(template(currentStage.view()))
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