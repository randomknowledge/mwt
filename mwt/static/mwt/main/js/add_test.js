$(document).ready(function(){
    if( window.view_name == 'add_test' )
    {
        var schedule_id = 0;
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

        $('.btn-boolean').click(function(event){
            event.preventDefault();
        });

        $('#main_form').submit(function(event){
            event.preventDefault();
            submitForm();
        });

        $('#add-schedule-button').click(function(event){
            event.preventDefault();
            schedule_id++;
            tpl = $('#schedule-template').html().replace(/\[id\]/g, schedule_id);
            $(this).after($(tpl));

            $('.close-schedule').unbind('click');
            $('.close-schedule').click(function(event){
                event.preventDefault();
                $(this).parent().remove();
            });

            $('.btn-now').unbind('click');
            $('.btn-now').click(function(event){
                event.preventDefault();
                var me = this;
                var d = new Date();
                var curr_date = d.getDate();
                var curr_month = d.getMonth() + 1; //Months are zero based
                var curr_year = d.getFullYear();
                $(this).parent().find('.date').val(zerofill(curr_year,4) + '-' + zerofill(curr_month) + '-' + zerofill(curr_date));
                $(this).parent().find('.time').val(d.toTimeString().match( /^([0-9]{2}:[0-9]{2}:[0-9]{2})/ )[0]);
                setTimeout(function(){
                    $(me).removeClass('active');
                }, 100);
            });
        });

        function zerofill(n, numzeros)
        {
            if(numzeros == undefined)
            {
                numzeros = 2;
            }
            n = n + "";
            while(n.length < numzeros)
            {
                n = "0" + n;
            }
            return n;
        }

        function collect_form_data()
        {
            var active_plugins = {};
            var active_notifications = {};
            $('#plugins .plugin-button.active').each(function(){
                active_plugins[parseInt($(this).attr('data-id'))] = {};
            });
            $('#notifications .plugin-button.active').each(function(){
                active_notifications[parseInt($(this).attr('data-id'))] = {};
            });

            $('.plugin-options-accordion .accordion-group.active div.controls').each(function(){
                var key = $(this).attr('data-param');
                var id = parseInt($(this).attr('data-plugin-id'));
                active_plugins[id][key] = get_value_from_field($(this).find('.plugin-option-field'));
            });

            $('.notification-options-accordion .accordion-group.active div.controls').each(function(){
                var key = $(this).attr('data-param');
                var id = parseInt($(this).attr('data-plugin-id'));
                active_notifications[id][key] = get_value_from_field($(this).find('.plugin-option-field'));
            });

            var schedules   = [];
            $('.schedule').each(function(){
                if( $(this).parent().attr('id') != 'schedule-template' )
                {
                    schedules.push({
                        'date': $(this).find('.date').val(),
                        'time': $(this).find('.time').val(),
                        'repeat': $(this).find('.repeat').val()
                    });
                }
            });

            data = {
                'description': $('#description').val(),
                'plugins': active_plugins,
                'notifications': active_notifications,
                'schedules': schedules
            };

            return data;
        }

        function get_value_from_field(field)
        {
            switch(field[0].nodeName.toLowerCase())
            {
                case 'button':
                    return $(field).hasClass('active');
                break;

                default:
                    return field.val();
                break;
            }
        }


        function submitForm()
        {
            url = self.location.href;
            if( url.indexOf('?') > -1 )
            {
                url += "&ajax";
            } else {
                url += "?ajax";
            }

            $.ajax({
                url: url + "&data=" + JSON.stringify(collect_form_data()),
                type: 'GET',
                dataType: 'json',
                processdata: false,
                success: function( data, textStatus, jqXHR ) {
                    console.log( data );
                },
                error: function( jqXHR, textStatus, errorThrown )
                {
                    console.log( jqXHR, textStatus, errorThrown );
                }
            });
        }
    }
});