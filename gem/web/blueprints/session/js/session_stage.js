function createStageController(controller) {

    // Processes incoming message
    // param: data - view of stage
    function processMessage(data) {
        // stage changed. Lets stop timer
        controller.timer.stop()

        //
        var stageController = stages[data.stage.type]
        if (stageController) {
            stageController.data = data
            if (stageController.enter) { stageController.enter() }
        }

        lastStageType = data.stage.type
        renderStage(data)

        if (stageController) {
            if (stageController.register) { stageController.register() }
        }
    }

    function onUserInfoMessage(data) {
        user = data
    }

    // Private members

    var viewHtml = $("#stage-template").html()
    var proposalsHtml = $("#proposals").html()

    var template = Handlebars.compile(viewHtml)
    var proposals = JSON.parse(proposalsHtml)

    var stages = {}
    var lastStageType = null
    var user = {}

    stages["voting"] = votingStageController(controller)
    stages["commenting"] = commentingStageController(controller)
    stages["discussion"] = discussionStageController(controller)


    function render(view) {
        var stageController = stages[lastStageType]
        if (stageController) {
            var view = stageController.view ? stageController.view() : {}
            renderStage(Object.assign({}, stageController.data, view))
            if (stageController.register) { stageController.register() }
        }
    }

    function renderStage(data) {
        // provide some additional data for template
        data.stageType = function() { return data.stage.type }
        data.user = user

        // load cached proposal data if proposal id is provided
        if (data.proposal_id) {
            data.proposal = proposals[data.proposal_id]
        }

        // render template and apply to DOM
        var html = template(data)
        $("#stage").html(html)

        // some dynamic
        // TODO: extract to somewhere else
        if (data.stage.type == "votingresults") {
            $('.vote-details').popover({ trigger: "hover" })
        }
    }

    return {processMessage, onUserInfoMessage}
}