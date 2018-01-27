function createSessionsController() {
    var me = {}

    me.isConcreteSessionPage = function() {
        return /sessions\/.+/.test(location.pathname)
    }

    me.onManageSessionClicked = function(sessionId) {
        window.location.href = "/session/" + sessionId
    }

    me.onChangeSessionStatusClicked = function(sessionId, status) {
        ajax_put("/sessions/" + sessionId, {"status": status}, me.onSessionStatusChangedResponse);
    }

    me.onSessionStatusChangedResponse = function(data) {
    }

    me.setProposals = function(value) {
        controller.proposals = value;
    }

    me.refreshProposalsList = function() {
        var ids = me.proposals.map(function (i) { return i["_id"] });
        
        var html = me.proposalsTemplate({
            proposals: controller.proposals,
            empty: "No proposals added to session",
            showDelete: true
        })

        $("#proposals").html(html);
        $("#proposals-ids").val(ids);
        $(".session-remove-proposal").on("click", function (e) {
            var key = $(this).data("key");
            controller.removeProposal(key)
        })
        $('[data-toggle="tooltip"]').tooltip()

        $("#proposals").sortable({
            cursor: "move",
            stop: function () {
                var sids = $(".list-group-item").map(function (x) {
                    return $(this).data("id")
                }).toArray()
                console.log(sids)
                $("#proposals-ids").val(sids)
            }
        })
    }

    me.appendProposalToSession = function(proposalKey, proposalTitle) {
        me.proposals.push({title: proposalTitle, "_id": proposalKey})
        me.refreshProposalsList()
        me.closeAddProposalDialog()
    }

    me.onProposalSearch = function(term) {
        ajax_get("/proposals/search", {"term": term}, me.onProposalSearchResponse);
    }

    me.onProposalSearchResponse = function(result) {
        var html = me.proposalsTemplate({
            proposals: result,
            empty: "Nothing found"});
        $("#proposal-search-result").html(html);
    }

    me.showAddProposalDialog = function() {
        me.proposalAddDialog.modal()
    }

    me.closeAddProposalDialog = function() {
        $("#proposal-search").val("");
        $("#proposal-search-result").empty();
        $("#proposal-add-modal").modal("hide");
    }

    me.removeProposal = function(proposalKey) {
        me.proposals = me.proposals.filter(function (i) { return i["_id"] != proposalKey })
        me.refreshProposalsList()
    }


    if (me.isConcreteSessionPage()) {
        var source = $("#entry-template").html()
        var source2 = $("#proposals-models").html()

        me.proposals = JSON.parse(source2)
        me.proposalsTemplate = Handlebars.compile(source)
        me.proposalAddDialog = $('#proposal-add-modal')
    }

    return me;
}

$(document).ready(function() {
    controller = createSessionsController();

    if (controller.isConcreteSessionPage()) {
        controller.refreshProposalsList();
    }

    $(".run").on("click", function() {
        var sessionId = $(this).data("key");
        controller.onChangeSessionStatusClicked(sessionId, "run");
    })

    $(".stop").on("click", function() {
        var sessionId = $(this).data("key");
        controller.onChangeSessionStatusClicked(sessionId, "closed");
    })

    $(".manage").on("click", function() {
        var sessionId = $(this).data("key");
        controller.onManageSessionClicked(sessionId);
    })

    $("#proposal-add").on("click", function() {
        controller.showAddProposalDialog();
    });

    $("#proposal-search").on("keyup", function() {
        var term = $("#proposal-search").val();
        if (term.length < 3) return;
        controller.onProposalSearch(term);
    });

    $("#proposal-search-result").on("click", "a", function(e) {
        e.preventDefault();
        var key = $(this).data("key");
        var title = $(this).text();

        if (key) {
            controller.appendProposalToSession(key, title);
        }
    });
});
