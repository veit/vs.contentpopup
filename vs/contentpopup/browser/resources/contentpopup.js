(function($) {

$(document).ready(function() {

    var actual_url = document.location.href;

    /* 
     * Image popup 
     */

    $('.captioned img,img.captioned').each(function(i) {
        var src = $(this).attr('src');
        $(this).attr('src',  src.replace('/index_html', ''));

        var parts = src.split('/');
        
        if (src.indexOf('@@images')>=0) {
            /* e.g. ajung.gif/@@images/1bc922b8-ca26-4b50-a9f6-3524e46fde36.jpeg */
            src = parts.slice(0, parts.length-2).join('/');
        }
        else {
            // remove trailing scale
            var scale = parts[parts.length-1];
            if (scale == 'index_html')  {
                /* e.g. path/to/content/some.jpg/index_html */
                src = parts.slice(0, parts.length-1).join('/');
            }
            else if (scale.indexOf('image_') > -1 || scale == 'image') {
                src = parts.slice(0, parts.length-1).join('/');
            }
        }
        src = src.replace('/index_html', '');
        $(this).after('<span class="magnify"></span>'); 
        $(this).next().andSelf().wrapAll('<a class="img-fullscreen" href="' + src + '/@@image_fullscreen_overlay"></a>');
    });

    $('.img-fullscreen').each(function(i) {
        var anchor = $(this);
        anchor.prepOverlay({
                subtype: 'ajax',
                width: 'auto'
            }
        );
    });

    /*
     * Table overlay
     */

    $('table.table-popup').each(function(i) {
        var table = $(this);
        var id = table.attr('id');
        var parents = $(this).closest("[documentroot='1']");
        if (parents.length == 1) {
            var parent_uid = parents[0].attributes['documentuid'].value;
            caption = table.find('caption');
            caption_text = caption.html();
            caption_text = caption_text==null ? '' : caption_text;
            $('<a class="table-popup" href="' + actual_url + '/@@show_table?uid=' + parent_uid + '&id=' + id +'")">' + caption_text + '</a>').insertBefore(table);
            table.hide();
        }
    });

    $('a.table-popup').each(function(i) {
        var anchor = $(this);
        anchor.prepOverlay({
                subtype: 'ajax',
                width: '90%'
            }
        );
    });
});

}(jQuery));
