/* Voting stage controller
 *
 * param session: session
 */
function VotingStageController(session) {

    console.log("CREATE")

    function register() {
        $("#vote-private").on("change", onSecretBallotCheckboxChanged)
        $(".vote").on("click", onVoteButtonClicked)
        session.timer.on(onTimerTick)
    }

    function unregister() {
        session.timer.off(onTimerTick)
    }

    function view() {
        console.log("VIEW", timeIsOver)
        return { voteStatus: voteStatus, timeIsOver }
    }

    // Private members

    var voteStatus = null // user's vote status
    var timeIsOver = false

    // handlers

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
        session.stage.render()
    }

    function onTimerTick(value) {
        if (value <= 0 && !timeIsOver) {
            timeIsOver = true
            session.stage.render()
        } else if (value > 0 && timeIsOver) {
            timeIsOver = false
            session.stage.render()
        }
    }

    // Actions

    function vote(value) {
        session.emit("vote", {value: value}, onVoteResponse)
    }

    function setVotingPrivacy(value) {
        session.emit("manage", {private: value})
    }

    return { register, unregister, view }
}