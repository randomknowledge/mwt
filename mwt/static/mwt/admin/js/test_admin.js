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
        function findPluginRows(id)
        {
            found = [];
            rows    = $('#test-group .form-row.dynamic-test :selected');
            for( var i = 0; i < rows.length; i++ )
            {
                if( $(rows[i]).val() == id )
                {
                    found.push( $(rows[i]).parent().parent().parent()[0] );
                }
            }
            return found;
        }

        function findUnassignedRows()
        {
            found = [];
            rows    = $('#test-group .form-row.dynamic-test :selected');
            for( var i = 0; i < rows.length; i++ )
            {
                if( $(rows[i]).val() == '' )
                {
                    found.push( $(rows[i]).parent().parent().parent()[0] );
                }
            }
            return found;
        }

        function checkPluginId(id)
        {
            plugin_id = id;
            if( plugin_params[plugin_id] )
            {
                pluginrows = findPluginRows(plugin_id);
                params = plugin_params[plugin_id].slice(0);

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
                    if( plugin_params[plugin_id].indexOf(key) == -1 )
                    {
                        var p = params.shift();
                        pluginrow.find('.field-key input').val(p);
                    }
                }

                if( params.length )
                {
                    pluginrows = findUnassignedRows();
                    for( j = 0; j < pluginrows.length; j++ )
                    {
                        pluginrow = $(pluginrows[j]);
                        pluginrow.find('.field-plugin select').val(plugin_id);
                        $('#id_plugins').change();
                    }
                }

                if( params.length )
                {
                    $('#test-group .add-row a').click();
                    $('#id_plugins').change();
                }
            }
        }

        $('#id_plugins').change(function(event){
            vals = $(this).val();
            if( vals != null )
            {
                for( var i = 0; i < vals.length; i++ )
                {
                    checkPluginId(vals[i]);
                }
            }
        });
    });
})(django.jQuery);
