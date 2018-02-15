function PrintDocumentWidget() {

    function setType(value) {
        type = value
    }

    function setArgs(value) {
        args = value
    }

    function setOptions(value) {
        options = value
        console.log(value)
    }

    function view() {
        return {
            type: type,
            args: JSON.stringify(args),
            options: JSON.stringify(options)
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

        var data = {
            type, args, options
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

    var type
    var args
    var options

    return { view, register, setType, setArgs, setOptions }
}
