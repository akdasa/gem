/* Acquaintance stage controller
 * Provides basic functionality
 * param session: session
 */
function AcquaintanceStageController(session) {

    function setState(value) {
        state = value
        console.log(value)
    }

    function register() {
        $(".selectpicker").selectpicker()
    }

    function view() {
        var roles = state.comments.map(function(obj) { return obj.role })
        roles = roles.filter(function(v, i) { return roles.indexOf(v) == i })

        return Object.assign(state, {
            "comments": {
                "comments": state.comments,
                "roles": roles
            }
        })
    }

    // Private members

    var state = null

    return { view, setState, register }
}
