class @Tests
  constructor: (@name) ->
    $("*[data-rel=popover]").popover()
    $("*[rel=tooltip]").tooltip()
    $("*[rel=lightbox]").click (event) ->
      event.preventDefault()
      $(@).colorbox
        iframe: true
        rel: "nofollow"
        speed: 0
        width: "95%"
        height: "95%"

    $(window).resize (event) ->
      $.colorbox.resize
        width: Math.round(95 * $(window).width() / 100)
        height: Math.round(95 * $(window).height() / 100)