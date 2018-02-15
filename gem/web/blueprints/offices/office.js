/* Office controller */

function OfficeController(options) {

    function register() {
        $(".office-order").on("click", onOrderClicked)
    }

    //

    function order(id, commentary) {
        console.log(id, commentary)
        ajax_post("/offices/" + officeId + "/order", { id, commentary }, onOrderResponse)
    }

    //

    function onOrderClicked(e) {
        e.preventDefault()

        var id = $(this).data("service-id")
        var name = $(this).data("service-name")

        alerts.input({
            title: "Order",
            message: name,
            placeholder:"Commentary (optional)",
            data: {id}}, onOrderSubmit)

    }

    function onOrderSubmit(msg, data) {
        order(data.id, msg)
    }

    function onOrderResponse(response) {
        if (response.success) {
            alerts.alert({message: "Your order has been submitted"})
        } else {
            alerts.alert({message: "Something goes wrong. Sorry."})
        }
    }

    //

    var alerts = Alerts()
    var officeId = options.officeId

    return { register }
}