/* Office admin controller */

function OfficeAdminController(options) {

    function register() {
        $("#office-admin-service-add").on("click", onAddServiceClicked)
    }

    //

    function addService(name) {
        var url = "/offices/" + officeId + "/admin/configure"
        ajax_post(url, { name }, onAddServiceResponse)
    }

    //

    function onAddServiceClicked(e) {
        e.preventDefault()
        var name = alerts.input({
            message: "Service name",
            title: "Add Service"},
            addService)
    }

    function onAddServiceResponse(response) {
        if (response.success) {
            alerts.alert({message: "Your service has been added"})
        } else {
            alerts.alert({message: "Something goes wrong. Sorry."})
        }
    }

    //

    var alerts = Alerts()
    var officeId = options.officeId

    return { register }
}