/* Voting Stage Controller
 *
 * param session: session
 */
function VotingStageController(session) {

    function setState(value) {
        state = value
    }

    function register() {
        $("#vote-private").on("change", onSecretBallotCheckboxChanged)
        $(".vote").on("click", onVoteButtonClicked)
        $(".selectpicker").selectpicker({
            style: 'btn-info btn-xs',
            size: 4, width: "100px"
        })
        $("#vote-threshold").on("changed.bs.select", onVoteThresholdChanged)
        session.timer.on(onTimerTick)
    }

    function unregister() {
        session.timer.off(onTimerTick)
    }

    function enter() {
        var timerValue = session.timers.get("voting")
        session.timer.start(timerValue)
    }

    function view() {
        var permissions = session.user.permissions

        return Object.assign(state, {
            voteStatus: voteStatus, timeIsOver,
            quorum: state.quorum,
            isFinalVote: state.type == "final",
            isVoteSubmitted: voteStatus.success == true,
            isVoteNotAccepted: voteStatus.success == false,
            isVoteChanged: voteStatus.prev && voteStatus.prev != voteStatus.value,
            vote: voteViewName(voteStatus.value),
            prevVote: voteViewName(voteStatus.prev),
            canVote: !timeIsOver && permissions.indexOf("vote") != -1,
            canManage: permissions.indexOf("vote.manage") != -1,
            privateChecked: state.private ? "checked" : "",
            showPrivateAlert: state.private && permissions.indexOf("vote") != -1,
            noQuorum: state.type == "final" && state.can_vote < state.quorum,
            threshold: state.threshold,
            selectedThreshold: function(val) { return val == state.threshold ? "selected" : ""}
        })
    }

    // Private members

    var state = null
    var voteStatus = {success:undefined, prev:undefined, value:undefined} // user's vote status
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
        session.stage.requestRender()
    }

    function onTimerTick(value) {
        if (value <= 0 && !timeIsOver) {
            timeIsOver = true
            session.stage.requestRender()
        } else if (value > 0 && timeIsOver) {
            timeIsOver = false
            session.stage.requestRender()
        }
    }

    function onVoteThresholdChanged(e) {
        var threshold = $(e.currentTarget).val()
        setVotingThreshold(threshold)
    }

    // Actions

    function vote(value) {
        session.emit("vote", {value: value}, onVoteResponse)
    }

    function setVotingPrivacy(value) {
        session.emit("manage", {cmd: "set_private", value: value})
    }

    function setVotingThreshold(value) {
        session.emit("manage", {cmd: "set_threshold", value: value})
    }

    function voteViewName(value) {
        if (value == "yes") return "In Favor"
        if (value == "no") return "Against"
        if (value == "undecided") return "Abstention"
        return value
    }

    return { register, unregister, view, setState, enter }
}