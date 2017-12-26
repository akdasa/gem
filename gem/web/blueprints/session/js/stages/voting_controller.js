function votingStageController(controller) {
    voteStatus = null;

    function register() {
        $("#vote-private").on("change", onSecretBallotCheckboxChanged)
        $(".vote").on("click", onVoteButtonClicked)
    }

    function view() {
        return {voteStatus: voteStatus}
    }

    function onSecretBallotCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setVotingPrivacy(val)
    }

    function onVoteButtonClicked(e) {
        e.preventDefault()
        var value = $(this).data("vote")
        vote(value)
    }

    function onVoteResponse(response) {
        voteStatus = response
        controller.render()
    }

    function setVotingPrivacy(value) {
        controller.socket.emit("manage", {private: value})
    }

    function vote(value) {
        controller.socket.emit("vote", {value: value}, onVoteResponse)
    }

    return { register, view }
}