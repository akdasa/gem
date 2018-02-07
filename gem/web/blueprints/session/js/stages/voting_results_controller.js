/* Voting Results Stage Controller
 *
 * param session: session
 */
function VotingResultsStageController(session) {

    function register() {
        $(".vote-details").popover({ trigger: "hover" })
    }

    function setState(value) {
        state = value
        votingResultsWidget.setResults(value)
    }

    function view() {
        return Object.assign({}, state, {
            voting: votingResultsWidget.view()
        })
    }

    var state
    var votingResultsWidget = VotingResultsWidget()

    return { view, setState, register }
}
