$(document).ready(function(){
    if( window.view_name == 'tests' )
    {
        $('*[data-rel=popover]').popover();
        $('*[rel=tooltip]').tooltip();
        $('*[rel=lightbox]').click(function(event){
            event.preventDefault();
            $(this).colorbox({
                iframe:true,
                width:"95%",
                height:"95%",
                scrolling: false
            });
        });

        $(window).resize(function(event){
            $.colorbox.resize({
                width: $(window).width() - 20,
                height: $(window).height() - 20
            });
        });
    }
});