$(function () {
    $("button.opinion").click(function (event) {
        event.preventDefault();
        const opinion_array = $(this).attr("id").split(" ");
        var opinion = {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            opinion: opinion_array[0],
            kind: opinion_array[1],
            id: opinion_array[2],
        };

        $.post("/api/opinion/", opinion).always(function (data, status) {
            console.log(data);
            console.log("Data: " + data['name'] + "\nStatus: " + status);
        });
    });
});
