$(function () {
    $("button.opinion").click(function (event) {
        event.preventDefault();
        const $this = $(this);
        const $parent = $this.parent("div.parent");
        if ($this.is("button:first-child")) {
            var $pare = $parent.find("button.opinion:last-child");
        } else {
            var $pare = $parent.find("button.opinion:first-child");
        }
        $this.prop("disabled", true);
        $pare.prop("disabled", true);
        const $id = $this.attr("id");
        const opinion_array = $id.split(" ");
        var opinion = {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            opinion: opinion_array[0],
            kind: opinion_array[1],
            id: opinion_array[2],
        };

        $.post("/api/opinion/", opinion).always(function (data) {
            if (data["create"]) {
                $this.addClass("active");
            } else if (data["delete"]) {
                $this.removeClass("active");
            } else if (data["update"]) {
                $this.addClass("active");
                $pare.removeClass("active");
            }
            $parent.find("button.opinion:first-child > span.badge").html(data["like"]);
            $parent.find("button.opinion:last-child > span.badge").html(data["dislike"]);
            $this.prop("disabled", false);
            $pare.prop("disabled", false);
        });
    });
});
