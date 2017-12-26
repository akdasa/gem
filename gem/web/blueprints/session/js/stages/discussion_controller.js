function discussionStageController(controller) {
    function register() {
        $(".discussion-give-voice").on("click", giveVoiceUserClicked)
        $("#discussion-raise-hand").on("click", raiseHandButtonClicked)
        $("#discussion-withdraw-hand").on("click", withdrawHandButtonClicked)
    }

    function giveVoiceUserClicked(e) {
        e.preventDefault();
        var userId = $(this).data("user-id")
        giveVoice(userId)
    }

    function raiseHandButtonClicked(e) {
        controller.socket.emit("manage", { command: "raise_hand" })
    }

    function withdrawHandButtonClicked(e) {
        controller.socket.emit("manage", { command: "withdraw_hand" })
    }

    function giveVoice(userId) {
        controller.socket.emit("manage", {command: "give_voice", user_id: userId})
    }

    return { register }
}
