class @Utils
  constructor: () ->
  @getUrl: () ->
    window.location.href

  @getAjaxUrl: () ->
    url = @getUrl()
    if url.indexOf('?') > -1
      url += "&ajax"
    else
      url += "?ajax"
    url

  @zerofill = (n, numzeros) ->
    numzeros = 2  if not numzeros?
    n = n + ""
    n = "0" + n  while n.length < numzeros
    n