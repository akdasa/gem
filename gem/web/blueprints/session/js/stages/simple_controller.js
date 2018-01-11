/* Simple stage controller
 * Provides basic functionality
 * param session: session
 */
function SimpleStageController(session) {

    function setState(value) {
        state = value
    }

    function view() {
        return state
    }

    // Private members

    var state = null

    return { view, setState }
}
