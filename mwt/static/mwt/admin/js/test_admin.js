if( !Array.indexOf )
{
    Array.prototype.indexOf = function(obj, start) {
        for (var i = (start || 0); i < this.length; i++) {
            if (this[i] == obj) {
                return i;
            }
        }
        return -1;
    }
}

(function($) {
    $(document).ready(function(){
        function findPluginRows(id, type)
        {
            var base;
            if( type == 'tasks' )
            {
                base    = $("h2:contains('Task plugin')").parent();
            } else {
                base    = $("h2:contains('Notification plugin')").parent();
            }
            found = [];
            rows    = base.find('tbody tr.form-row').not('.empty-form').find('.field-plugin option:selected');
            for( var i = 0; i < rows.length; i++ )
            {
                if( $(rows[i]).val() == id )
                {
                    found.push( $(rows[i]).parent().parent().parent()[0] );
                }
            }

            return found;
        }

        function findUnassignedRows(type)
        {
            found = [];
            var base;
            if( type == 'tasks' )
            {
                base    = $("h2:contains('Task plugin')").parent();
            } else {
                base    = $("h2:contains('Notification plugin')").parent();
            }
            rows    = base.find('tbody tr.form-row').not('.empty-form').find('.field-plugin option:selected');
            for( var i = 0; i < rows.length; i++ )
            {
                if( $(rows[i]).val() == '' )
                {
                    found.push( $(rows[i]).parent().parent().parent()[0] );
                }
            }
            return found;
        }

        function checkPluginId(id, type)
        {
            plugin_id = id;
            if( plugin_params[type][plugin_id] )
            {
                pluginrows = findPluginRows(plugin_id, type);
                params = plugin_params[type][plugin_id].slice(0);

                $(pluginrows).each(function(idx, ele){
                    var index   = params.indexOf($(ele).find('.field-key input').val());
                    if( index != -1 )
                    {
                        params.splice(index,1);
                    }
                });

                if( !params.length )
                {
                    return;
                }

                for( var j = 0; j < pluginrows.length; j++ )
                {
                    if( params.length == 0 )
                    {
                        break;
                    }
                    var pluginrow = $(pluginrows[j]);
                    var key = pluginrow.find('.field-key input').val();
                    if( plugin_params[type][plugin_id].indexOf(key) == -1 )
                    {
                        var p = params.shift();
                        pluginrow.find('.field-key input').val(p);
                    }
                }

                if( params.length )
                {
                    pluginrows = findUnassignedRows(type);
                    for( j = 0; j < pluginrows.length; j++ )
                    {
                        pluginrow = $(pluginrows[j]);
                        pluginrow.find('.field-plugin select').val(plugin_id);
                        $('#id_' + type).change();
                    }
                }

                if( params.length )
                {
                    if(type == 'tasks')
                    {
                        $("h2:contains('Task plugin')").parent().find('tr.add-row a').click();
                    } else {
                        $("h2:contains('Notification plugin')").parent().find('tr.add-row a').click();
                    }
                    $('#id_' + type).change();
                }
            }
        }

        $('#id_tasks, #id_notifications').change(function(event){
            vals = $(this).val();
            var type = $(this).attr('id').replace(/^id_/,'');
            if( vals != null )
            {
                for( var i = 0; i < vals.length; i++ )
                {
                    checkPluginId(vals[i], type);
                }
            }
        });
    });
})(django.jQuery);
