var myApp = {
    init: function() {
        var $slider = $('.effects');
        var width = $("li.effect-box").width() * $('ul.effects li').length + 500;
        $slider.attr('width', width);
    },
    saveEditedPic: function() {
        // $("[name=csrfmiddlewaretoken]").val($('.editor').attr('src'))
        // $("#filepath").submit();
        console.log("{{ csrf_token }}")
        $.ajax({
            type: 'POST',
            url: '/save-effects/',
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                'path': $('.editor').attr('src'),
            },
            success: function(data) {
                $(".wrapper").load("/ .image-collection", function() {
                    $('.wrapper').on('click', 'img', myApp.prepareCanvas)
                    $(".thumbholder").on('click', '.delete', myApp.deleteImage)
                });
            },
        });
    },
    applyEffects: function() {
        // prepares an image for editing
        var effect = $(this).text();
        var pic_path = $(".editor").attr("src");
        $('#loading-indicator').show();
        $.ajax({
            type: 'GET',
            url: '/image/',
            data: {
                'effect': effect,
                'path': pic_path,
            },
            success: function(data) {
                $(".editor").attr("src", data);
                $(".editor").fadeIn().delay(200)
                $("#download").attr("href", data);
                $('#loading-indicator').hide();
            },
        });
    },
    prepareCanvas: function(e) {
        e.preventDefault();

        var thumb = $(this).attr("src");
        var src = $(this).attr("data");
        $(".editor").attr("src", src);
        $("#download").attr("href", src);
        var resource = window.location.origin + src
        $(".fb-share-button").attr("data-href", resource)
        FB.XFBML.parse()
        console.log(resource)
        var getThumb = function(effect, pic_path, $li) {
            $.ajax({
                type: 'GET',
                url: '/image/',
                data: {
                    'effect': effect,
                    'path': pic_path,
                    'preview': true,
                },
                success: function(data) {
                    console.log(data)

                    $li.css('background-image', 'url("' + data + '")')
                },
            });
        }
        $(".effects li").each(function(index) {
            $li = $(this)
            var effect = $(this).text();
            var pic_path = thumb;
            getThumb(effect, pic_path, $li);
        });
    },
    deleteImage: function() {
        // set modal to display picture for deleting
        var img = $(this).parents(".thumbholder").find("img").attr("data")
        $(".del-image").attr("src", img)
        $(".del-image").attr("id", $(this).attr('id'))
    },
    // onclick of modal delete images
    confirmedDelete: function() {
        url = "/image/" + $(".del-image").attr("id") + "/delete"
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                $(".wrapper").load("/ .image-collection", function() {
                    $('.wrapper').on('click', 'img', myApp.prepareCanvas)
                    $(".thumbholder").on('click', '.delete', function(e) {
                        var img = $(this).parents(".thumbholder").find("img").attr("data")
                        e.preventDefault();
                        $(".del-image").attr("src", img)
                        $(".del-image").attr("id", $(this).attr('id'))
                    })
                });
            }
        })
    },
}
$(document).ready(function() {
    myApp.init();
    $('ul.effects').on('click', 'li', myApp.applyEffects);
    $('.wrapper').on('click', 'img', myApp.prepareCanvas);
});

// saves edited photos
$(".photo-icons").on('click', '.img-save', myApp.saveEditedPic)
    // Triggers modal to appear
$(".thumbholder").on('click', '.delete', myApp.deleteImage)
    // Handles when delete confirmation is made
$("#submit").on('click', myApp.confirmedDelete)
    // Puts image on canvas
