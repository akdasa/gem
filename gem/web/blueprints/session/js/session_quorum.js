/* Quorum controller. */
function QuorumController(session) {


    function requestChange() {
        showChangeQuorumDialog()
    }

    // Private members

    var quorum = 19

    function showChangeQuorumDialog() {
        Alerts().input("Change Quorum", "Quorum", sendQuorumChangeRequest)
    }

    function sendQuorumChangeRequest(value) {
        session.emit(
            "manage_session",
            { command: "set_quorum", value },
            onQuorumChangeRequestResponse)
    }

    // Handlers

    function onQuorumChangeRequestResponse(response) {

    }

    return { requestChange }
}