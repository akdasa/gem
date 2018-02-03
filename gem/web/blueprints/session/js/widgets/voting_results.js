/* Voting Results Widget
 *
 * Displays results of ballot
 */
function VotingResultsWidget() {

    // Sets results of ballot to display
    // param value: results of ballot
    function setResults(value) {
        state = value
    }

    // Sets visibility of widget
    // param value: true - widget is visible, otherwise false
    function setVisibility(value) {
        showWidget = value
    }

    // Returns view state of widget
    function view() {
        return Object.assign({}, state, {
            showWidget,
            isPasses: state.status == "pass",
            isFailed: state.status == "fail",
            isTied: state.status == "tie",
            isFinalVote: state.type == "final"
        })
    }

    var showWidget = true
    var state

    return { setResults, setVisibility, view }
}
