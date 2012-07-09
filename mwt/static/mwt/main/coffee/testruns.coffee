class @Testruns
  constructor: (@name) ->
    if window.announce
      announce.on 'notifications', (do =>
        @loadTestrunData)
      announce.init()
    else
      setInterval (do =>
        @loadTestrunData), 5000

  loadTestrunData: () ->
    $.ajax Utils.getAjaxUrl(),
      dataType: 'json'
      success: (data, rest...) ->
        if data.num_pages > window.num_pages
          window.location.reload()
        else
          $('#runs').children().remove()
          for item in data.items
            $('#runs').append($(item.html))
      error: (args...) -> console.log args...
