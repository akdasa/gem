function DiscussionStageController(controller) {
    var state

    function register() {
        $("#discussion-accept").on("change", onAcceptCheckboxChanged)
        $(".discussion-give-voice").on("click", onGiveVoiceToUserClicked)
        $(".discussion-remove").on("click", onRemoveUserFromQueueClicked)
        $("#discussion-raise-hand").on("click", onRaiseHandButtonClicked)
        $("#discussion-withdraw-hand").on("click", onWithdrawHandButtonClicked)
        $("[data-toggle='tooltip']").tooltip()
    }

    function setState(value) {
        state = value
    }

    function view() {
        return state
    }

    function onAcceptCheckboxChanged(e) {
        var value = $(this).is(":checked")
        acceptApplications(value)
    }

    function onGiveVoiceToUserClicked(e) {
        e.preventDefault()
        var userId = $(this).data("user-id")
        giveVoice(userId)
    }

    function onRemoveUserFromQueueClicked(e) {
        e.preventDefault()
        var userId = $(this).data("user-id")
        remove(userId)
    }

    function onRaiseHandButtonClicked(e) {
        e.preventDefault()
        raiseHand()
    }

    function onWithdrawHandButtonClicked(e) {
        e.preventDefault()
        withdrawHand()
    }

    // Actions

    function acceptApplications(value) {
        controller.socket.emit("manage", {command: "accept", value: value})
    }

    function giveVoice(userId) {
        controller.socket.emit("manage", {command: "give_voice", user_id: userId})
    }

    function remove(userId) {
        controller.socket.emit("manage", {command: "remove", user_id: userId})
    }

    function raiseHand() {
        controller.socket.emit("manage", { command: "raise_hand" })
    }

    function withdrawHand() {
        controller.socket.emit("manage", { command: "withdraw_hand" })
    }

    return { register, view, setState }
}
