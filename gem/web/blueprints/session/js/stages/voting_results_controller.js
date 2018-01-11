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
    }

    function view() {
        return state
    }

    var state = null

    return { view, setState, register }
}
