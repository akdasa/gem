/* Acquaintance stage controller
 * Provides basic functionality
 * param session: session
 */
function AcquaintanceStageController(session) {

    function setState(value) {
        state = value

        // get unique roles
        roles = state.comments.map(function(obj) { return obj.role })
        roles = roles.filter(function(v, i) { return roles.indexOf(v) == i })
    }

    function register() {
        $(".selectpicker").selectpicker()
        $(".vote-details").popover({ trigger: "hover" })
    }

    function view() {
        return Object.assign(state, {
            "comments": {
                "comments": state.comments,
                "roles": roles
            }
        })
    }

    // Private members

    var state = null
    var roles = []

    return { view, setState, register }
}
