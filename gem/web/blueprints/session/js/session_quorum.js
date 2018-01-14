/* Quorum controller. */
function QuorumController(session) {

    function requestChange() {
        showChangeQuorumDialog()
    }

    function showQuorumChangeCode(data) {
        alerts.alert({
            title: "Quorum Change Code",
            message: data.code
        })
    }

    // Private members

    var alerts = Alerts()

    function showChangeQuorumDialog() {
        alerts.input({
            title: "Change Quorum",
            placeholder: "New Quorum"},
            onChangeQuorumDialogValueEntered)
    }

    function sendQuorumChangeRequest(value) {
        session.emit(
            "manage_session",
            { command: "set_quorum", value: Number(value) },
            onQuorumChangeRequestResponse)
    }

    function sendQuorumChangeCodes(value) {
        session.emit(
            "manage_session",
            { command: "set_quorum", codes: value },
            onQuorumChangeCodesResponse
        )
    }

    // Handlers
    function onChangeQuorumDialogValueEntered(value) {
        if (!Number.isInteger(Number(value))) {
            alerts.alert({
                title: "Value is not valid",
                message: "Please provide positive integer value"
            })
        } else {
            sendQuorumChangeRequest(value)
        }
    }

    function onQuorumChangeRequestResponse(response) {
        var names = response.users.join(", ")
        alerts.input({
            title: "Change Quorum",
            message: "Waiting codes from: " + names,
            placeholder: "Each code on a new line"},
            onQuorumCodeEntered)
    }

    function onQuorumCodeEntered(value) {
        var codesArray = value
            .split(/\s+/g)  // split by whitespace
            .filter(Number) // get numbers only
            .map(function(x) { return Number(x) }) // convert to numbers
        sendQuorumChangeCodes(codesArray)
    }

    function onQuorumChangeCodesResponse(response) {
        if (response.success) {
            alerts.alert({title: "Change Quorum", message: response.message})
        } else {
            alerts.alert({title: "Change Quorum", message: response.message})
        }
    }

    return { requestChange, showQuorumChangeCode }
}