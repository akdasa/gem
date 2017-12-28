function createChatController(controller) {

    var messagesPanel = $("#messages")
    var messageInput = $("#chat-message")

    $("#chat-message").keypress(function (e) {
        if (e.which != 13) return

        var msg = messageInput.val()
        messageInput.val("")
        say(msg)
        return false
    })

    function processMessage(data) {
        append(data)
    }

    function say(message) {
        controller.socket.emit("chat", { msg: message });
    }

    function append(data) {
        messagesPanel.append("<li>" + data["who"] + ": " + data["msg"] + "</li>")
    }

    return { processMessage, say }
}