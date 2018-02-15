/* Comments Filter Widget
 *
 * Options:
 *   onFilterChanged: raises when filter changed
 *
 * Methods:
 *   setRoles: sets list of roles to choose from
 */
function CommentsFilterWidget(options) {

    // Set roles to choose from
    // param value: array of roles
    function setRoles(value) {
        roles = value

        if (!selectedRoles) selectedRoles = value
    }

    function view() {
        return {
            roles,
            typeSelected: isSelected(selectedTypes),
            roleSelected: isSelected(selectedRoles),
            sortSelected: isSelected(selectedSort)
        }
    }

    function register() {
        $("#comment-filter-type").on("changed.bs.select", onFilterChanged)
        $("#comment-filter-role").on("changed.bs.select", onFilterChanged)
        $("#comment-sort").on("changed.bs.select", onFilterChanged)
    }

    // Private members

    var roles = [] // list of roles to choose from
    var selectedRoles = null
    var selectedTypes = ["plus", "minus", "info"]
    var selectedSort = ["timestamp"]

    // Filter has been changed
    function onFilterChanged(e) {
        selectedTypes = $("#comment-filter-type").val()
        selectedRoles = $("#comment-filter-role").val()
        selectedSort = $("#comment-sort").val()

        if (options.onFilterChanged) {
            options.onFilterChanged({ types: selectedTypes,
                roles: selectedRoles, sort: selectedSort })
        }
    }

    function isSelected(array) {
        var lambda = function(name) {
            return array.indexOf(name) != -1 ? "selected" : ""
        }
        return lambda
    }

    return { view, setRoles, register }
}
