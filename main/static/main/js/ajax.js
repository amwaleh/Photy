$(document).ready(function() {
    // prepares an image for editing 
    $('ul.effects').on('click', 'li', function(e) {
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
                console.log(data);
                $(".editor").attr("src", data);
                $("#download").attr("href", data);
                $('#loading-indicator').hide();

            },

        });

    });

});
// sets width for the effect box
var $slider = $('.effects')
var width = $("li.effect-box").width() * $('ul.effects li').length + 500;
$slider.attr('width', width)


$(document).ready(function() {
    // populates the efects with the clicked image
    var sdata = ''
    $('.image-collection').on('click', 'img', function(e) {
        var thumb = $(this).attr("src");
        var src = $(this).attr("data");
        $(".editor").attr("src", src);
        $("#download").attr("href", src);
        $(".fb-share-button").attr("data-href",src)

        $(".effects li").each(function(index) {
            $li = $(this)
            var effect = $(this).text();
            var pic_path = thumb;
            get_thumb(effect, pic_path, $li)
        });


        $('.custom').on('click', function(e) {
            console.log('slider')
            console.log($(this.attr('id')))
        })

    });
    var get_thumb = function(effect, pic_path, $li) {
        console.log(pic_path)
        $.ajax({
            cache: false,
            type: 'GET',
            url: '/image/',
            data: {
                'effect': effect,
                'path': pic_path,
                'preview': true
            },
            success: function(data) {
                // var img = "<img src='" + data +"' width=100% height=100%>"
                //var effect = $(this).text('kil')
                $li.css('background-image', 'url("' + data + '")')
            },


        });
    }
});


$(document).ready(function() {

    $(".thumbholder").on('click', '.delete', function(e) {
        var img = $(this).parents(".thumbholder").find("img").attr("data")
        e.preventDefault();
        console.log(img);

        $(".del-image").attr("src", img)
        $(".del-image").attr("id", $(this).attr('id'))

    })

    // delete images
    $("#submit").on('click', function(e) {
        url = "/image/" + $(".del-image").attr("id") + "/delete"

        e.preventDefault();
        console.log(url)

        $.ajax({

            url: url,
            type: 'GET',

            success: function(data) {
                $(document).ready(function() {

                    $(".image-collection").load("/ .image-collection", function() {

                        $(".thumbholder").on('click', '.delete', function(e) {
                            var img = $(this).parents(".thumbholder").find("img").attr("data")
                            e.preventDefault();
                            console.log(img);

                            $(".del-image").attr("src", img)
                            $(".del-image").attr("id", $(this).attr('id'))

                        })

                    });
                })

            }


        })
    });
})
