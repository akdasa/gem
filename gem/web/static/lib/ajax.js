function ajax_post(url, data, callback) {
    $.ajax({
        url: url,
        type: 'POST',
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(data) {
            callback(data);
        }
    });
}

function ajax_put(url, data, callback) {
    $.ajax({
        url: url,
        type: 'PUT',
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(data) {
            callback(data);
        }
    });
}

function ajax_get(url, data, callback) {
    $.ajax({
        url: url,
        type: 'GET',
        contentType: "application/json",
        dataType: 'json',
        data: data,
        success: function(data) {
            callback(data);
        }
    });
}
