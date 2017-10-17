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
