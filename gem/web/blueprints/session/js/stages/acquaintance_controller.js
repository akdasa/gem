/* Acquaintance stage controller
 * Provides basic functionality
 * param session: session
 */
function AcquaintanceStageController(session) {

    function setState(value) {
        state = value
        console.log(value)
    }

    function view() {
        return state
    }

    // Private members

    var state = null

    return { view, setState }
}
