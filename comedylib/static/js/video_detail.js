$(document).ready(function() {
     /* Tooltip activation */
    $(function(){
       $('[rel="tooltip"]').tooltip();
    });
    /* Social sharing */
    // Facebook
    $('#fb_share_btn').click(function(e){
        e.preventDefault();
        var sharer = 'https://www.facebook.com/sharer/sharer.php?u=';
        window.open(sharer+location.href, 'sharer', 'width=626,height=436');
    });
    // Google Plus
    $('#gp_share_btn').click(function(e) {
        e.preventDefault();
        var sharer = 'https://plus.google.com/share?url=',
            uriArgs = 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600';
        window.open(sharer+pageAbsoluteURI, '', uriArgs);
    });
    // Reddit
    $('#rdt_share_btn').click(function(e) {
        e.preventDefault();
        var sharer = 'http://www.reddit.com/submit?url=',
            uriArgs = 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=700,width=550';
        window.open(sharer+pageAbsoluteURI, '', uriArgs);
    });

    /* Affiliate offers */
    $.get(affiliateOffersURI, {keyword: collectioName}, function(data) {
        var html = '<h2>Buy something with '+collectioName+'</h2>';
        for (var i=0; i < data.length; i++) {
            var prod_html = '<div class="col-xs-12 col-sm-6"><a target="_blank" href="'+ data[i].url +'"><img src="' + data[i].image_url +'" /></a>';
            prod_html += '<a class="title" target="_blank" href="'+ data[i].url +'">'+ data[i].title +'</a>';
            prod_html += '<p>'+ data[i].price +'</p></div>';
            html += prod_html;
        }
        $('div#affiliate').html(html);
    });

    /* Playlist handling */

    // Add video to playlist handling
    $("#addplay-btn").click(function() {
        if ($("#addtoplaycontent").is(":hidden")) {
            $("#addtoplaycontent").slideDown("normal");
            return false;
        } else {
            $("#addtoplaycontent").slideUp("normal");
            return false;
        }
    });
    $("#addtoplaycontent").hover(
        function() { mouseIsInside = true; },
        function() { mouseIsInside = false; }
    );
    $("body").click(function() {
        if (!mouseIsInside) {
            $("#addtoplaycontent").slideUp("fast");
        }
    });

    // Playlist creation
    function clearInput() {
        $("#playlistform :input").each(function() {
            $(this).val('');
        });
        $("#sub").val('Create playlist');
        $("#feedback").text('Your playlist has been created.').delay(1500).fadeOut();
    };
    $('#sub').on("click", function(event)  {
        event.preventDefault();
        $("#feedback").text('').fadeIn();
        $.post($("#playlistform").attr("action"), {'title': $('#id_title').val()}, function(data) {
            $('#playlistul').append('<li data-playlist-id="'+data.pk+'" class="active">'+$("#id_title").val()+' (0)</li>');
            clearInput();
        });
    });

    // Add video to playlist
    $(document).on("click", "#playlistul li.active", function(event){
        event.preventDefault();
        li = $(this);
        $.post(addToPlaylistURI, {'vid': videoId, 'pid': li.attr('data-playlist-id')}, function(data) {
            title = li.text();
            vidCount = title.match(/\((\d+)\)/)[1];
            newVidCount = (parseInt(vidCount) + 1).toString();
            newTitle = title.replace(/\(\d+\)/, '('+newVidCount+')');
            li.text(newTitle);
            li.addClass('inactive');
            li.removeClass('active');
        });
    });

    /* Autoplay */

    // Toggling the 'autoplay' button along with the variable
    // that specifies whether 'autoplay' should be enabled
    $('span.glyphicon-repeat').parent('a').click(function(event) {
        event.preventDefault();
        $('span.glyphicon-repeat').toggleClass('active');
        if (autoplay === true) {
            $.post(autoplayURI, {'autoplay': 0}, function(data) {
                autoplay = false;
            });
        } else {
            $.post(autoplayURI, {'autoplay': 1}, function(data) {
                autoplay = true;
            });
        }
    });
    // When the player is idle, we check if it has reached the end
    // of the video and redirect to the next one, if autoplay is
    // enabled
    jwplayer().onIdle(function(event) {
        if (autoplay === true) {
            var position = jwplayer().getPosition();
            var duration = jwplayer().getDuration();
            if ((duration - position) < 1) {
                window.location.href = nextVideoURI;
            }
        }
    });

    /* Liking */

    // Mapping between buttons and the feelings they express
    button_feel = {'like_btn': 'L', 'dislike_btn': 'D'};
    // Mapping between buttons and the loader images
    button_loader = {'like_btn': '#ll', 'dislike_btn': '#dl'};

    // Function that returns another function specific to
    // each pressed button
    var handlerFact = function(clicked_button, other_button) {
        var handler = function(event) {
            // Getting the button-specific loader
            event.preventDefault();
            var loader = $(button_loader[clicked_button.attr('id')]);

            loader.fadeIn('slow');
            if (clicked_button.hasClass('active')) {
                var feeling = 'U';
                var success = function() {
                    loader.fadeOut('slow');
                    clicked_button.removeClass('active');
                };
            } else {
                var feeling = button_feel[clicked_button.attr('id')];
                var success = function() {
                    loader.fadeOut('slow');
                    clicked_button.addClass('active');
                    other_button.removeClass('active');
                };
            }
            $.post(videoFeelingURI, {'vid': videoId, 'feeling': feeling})
                .done(success)
                .fail(function(){ alert('Ooops! Something went wrong.'); });
                //TODO: Do proper error handling
        };
        return handler;
    };
    var likeBtn = $('#like_btn'),
        dislikeBtn = $('#dislike_btn');

    // Binding each button click to its specific callback
    likeBtn.click(handlerFact(likeBtn, dislikeBtn));
    dislikeBtn.click(handlerFact(dislikeBtn, likeBtn));

    /* Bookmarking */
    var bookmarkStates = {
        'active': {
            'rmCl': 'active',
            'adCl': 'inactive',
            'text': 'Bookmark <span class="glyphicon glyphicon-minus"></span>',
            'titl': 'Remove this video from bookmarks',
            'url': addToBookmarksURI
        },
        'inactive': {
            'rmCl': 'inactive',
            'adCl': 'active',
            'text': 'Bookmark <span class="glyphicon glyphicon-plus"></span>',
            'titl': 'Save this video to watch later',
            'url': removeFromBookmarksURI
        },
            'active1': {
            'rmCl': 'active1',
            'adCl': 'inactive1',
            'text': 'Bookmark <span class="glyphicon glyphicon-list"></span>',
            'titl': 'Remove this playlist from bookmarks',
            'url': addToBookmarksURI
        },
        'inactive1': {
            'rmCl': 'inactive1',
            'adCl': 'active1',
            'text': 'Bookmark <span class="glyphicon glyphicon-list"></span>',
            'titl': 'Save this playlist to watch later',
            'url': removeFromBookmarksURI
        }
    }

    $('#bookmark_btn').click(function(event) {
        event.preventDefault();
        button = $(event.currentTarget);
        button_cls = button.attr('class');
        $.post(bookmarkStates[button_cls].url, {'id': videoId, 'obj': 'V'})
            .done(function() {
                button.removeClass(bookmarkStates[button_cls].rmCl);
                button.addClass(bookmarkStates[button_cls].adCl);
                button.html(bookmarkStates[button_cls].text);
                button.attr('title', bookmarkStates[button_cls].titl );
            })
            .fail(function() { alert('An error has occured'); });
            //TODO: Do proper error handling
    });
    if (inPl) {
        $('#bookmark_pl').click(function(event) {
            event.preventDefault();
            button = $(event.currentTarget);
            button_cls = button.attr('class');
            $.post(bookmarkStates[button_cls].url, {'id': currentPlId, 'obj': 'P'})
                .done(function() {
                    button.removeClass(bookmarkStates[button_cls].rmCl);
                    button.addClass(bookmarkStates[button_cls].adCl);
                    button.html(bookmarkStates[button_cls].text);
                    button.attr('title', bookmarkStates[button_cls].titl );
                })
                .fail(function() { alert('An error has occured'); });
                //TODO: Do proper error handling
        });
    }
    
});
