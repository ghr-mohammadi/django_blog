$(function () {
    $("br").addClass("d-none");

    var $id_tags = $("label[for=id_tags]");
    $("<span/>", {
        class: "ms-3",
        text: "اضافه کردن تگ",
    }).appendTo($id_tags);
    $("<button/>", {
        id: "add_tag",
        type: "button",
        class: "badge rounded-circle border-0 bg-primary ms-1",
        "data-bs-toggle": "modal",
        "data-bs-target": "#createTagModal",
        text: "+",
    }).appendTo($id_tags);

    $("button#btn_add_tag").click(function (event) {
        event.preventDefault();
        var tag_data = {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            name: $('input[name="add_tag"]').val(),
        };
        $.post("/api/create-tag/", tag_data).always(function (data) {
            location.reload();
        });
    });
});
