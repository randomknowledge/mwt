$(document).ready(function(){
    $('*[data-rel=popover]').popover();
    $('*[rel=tooltip]').tooltip();

    if( window.view_name == 'testruns' )
    {
        url = self.location.href;
        if( url.indexOf('?') > -1 )
        {
            url += "&ajax";
        } else {
            url += "?ajax";
        }
        setInterval(function(){
            $.ajax({
                url: url,
                dataType: 'json',
                success: function( data, textStatus, jqXHR ) {
                    if( data.num_pages > window.num_pages )
                    {
                        self.location.reload();
                        return;
                    }

                    $('#runs').children().remove();
                    for( var i = 0; i < data.items.length; i++ )
                    {
                        $('#runs').append($(data.items[i].html));
                    }
                },
                error: function( jqXHR, textStatus, errorThrown )
                {
                    console.log( jqXHR, textStatus, errorThrown );
                }
            });
        },5000);
    }
});