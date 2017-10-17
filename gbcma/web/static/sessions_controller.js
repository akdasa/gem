function onRunSessionClicked(sessionId) {
    ajax_put("/sessions/" + sessionId, {"status": "run"}, onRunSessionResponse);
}

function onStopSessionClicked(sessionId) {
    ajax_put("/sessions/" + sessionId, {"status": "stopped"}, onRunSessionResponse);
}


function onRunSessionResponse(data) {
    console.log(data);
}


$(document).ready(function() {
    $(".run").on("click", function() {
        var sessionId = $(this).data("key");
        onRunSessionClicked(sessionId);
    })

    $(".stop").on("click", function() {
        var sessionId = $(this).data("key");
        onStopSessionClicked(sessionId);
    })
});