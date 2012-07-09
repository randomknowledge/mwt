$(document).ready(function(){
    if( window.view_name == 'tests' )
    {
        $('*[data-rel=popover]').popover();
        $('*[rel=tooltip]').tooltip();
        $('*[rel=lightbox]').click(function(event){
            event.preventDefault();
            $(this).colorbox({
                iframe:true,
				rel: 'nofollow',
				speed: 0,
                width:"95%",
                height:"95%"
            });
        });

        $(window).resize(function(event){
            $.colorbox.resize({
                width: Math.round(95 * $(window).width() / 100),
                height: Math.round(95 * $(window).height() / 100)
            });
        });
    }
});