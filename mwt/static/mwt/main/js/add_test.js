$(document).ready(function(){
    if( window.view_name == 'add_test' )
    {
        $('.btn-group .btn').button();

        $('.form-actions button.cancel').click(function(event){
            event.preventDefault();
            $(parent.document).find('#cboxClose').click();
        });

        $('.plugin-button').click(function(event){
            event.preventDefault();
            var active = !$(this).hasClass('active');
            var id = $(this).attr('data-id');
            var base = 'plugin';
            if( $(this).hasClass('notification') )
            {
                base = 'notification';
            }
            $('#' + base + '-options-' + id).toggleClass('active', active);
        });
    }
});