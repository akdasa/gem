function PrintDocumentWidget(options) {

    function view() {
        return {
            type: options.type,
            args: JSON.stringify(options.args)
        }
    }

    function register() {
        $(".print-document").on("click", onPrintClicked)
    }

    function onPrintClicked(e) {
        e.preventDefault()

        var alert = Alerts().alert({
            title:"Printing",
            message:"We are printing your document. Please wait a moment."
        })

        console.log($(this).data("args"))

        var data = {
            type: $(this).data("type"),
            args: $(this).data("args")
        }

        controller.emit("print", data, function(data) {
            if (data.success) {
                $.fileDownload("/files/" + data.path)
                alert.close()
            } else {
                Alerts().alert({title: "Error", message: data.message})
            }
        })
    }

    return { view, register }
}
