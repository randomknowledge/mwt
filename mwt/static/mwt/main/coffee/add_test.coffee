class @Addtest
  constructor: (@name) ->
    schedule_id = 0

    $(".btn-group .btn").button()
    $(".form-actions button.cancel").click (event) ->
      event.preventDefault()
      $(window.parent.document).find("#cboxClose").click()

    $(".plugin-button").click (event) ->
      event.preventDefault()
      active = not $(@).hasClass("active")
      id = $(@).attr("data-id")
      base = "plugin"
      base = "notification"  if $(@).hasClass("notification")
      $("#" + base + "-options-" + id).toggleClass "active", active

    $(".btn-boolean").click (event) ->
      event.preventDefault()

    $("#main_form").submit (event) ->
      event.preventDefault()
      submitForm()

    $("#add-schedule-button").click (event) ->
      event.preventDefault()
      schedule_id++
      tpl = $("#schedule-template").html().replace(/\[id\]/g, schedule_id)
      $(event.currentTarget).after $(tpl)
      $(".close-schedule").unbind "click"
      $(".close-schedule").click (event) ->
        event.preventDefault()
        $(event.currentTarget).parent().remove()

      $(".btn-now").unbind "click"
      $(".btn-now").click (event) ->
        event.preventDefault()
        me = event.currentTarget
        d = new Date()
        curr_date = d.getDate()
        curr_month = d.getMonth() + 1
        curr_year = d.getFullYear()
        $(event.currentTarget).parent().find(".date").val Utils.zerofill(curr_year, 4) + "-" + Utils.zerofill(curr_month) + "-" + Utils.zerofill(curr_date)
        $(event.currentTarget).parent().find(".time").val d.toTimeString().match(/^([0-9]{2}:[0-9]{2}:[0-9]{2})/)[0]
        setTimeout (->
          $(me).removeClass "active"
        ), 100


  submitForm = ->
    url = Utils.getAjaxUrl()
    $.ajax
      url: url + "&data=" + JSON.stringify(collect_form_data())
      type: "GET"
      dataType: "json"
      processdata: false
      success: (data, textStatus, jqXHR) ->
        console.log data

      error: (jqXHR, textStatus, errorThrown) ->
        console.log jqXHR, textStatus, errorThrown


  collect_form_data = ->
    active_plugins = {}
    active_notifications = {}
    $("#plugins .plugin-button.active").each ->
      active_plugins[parseInt($(this).attr("data-id"))] = {}

    $("#notifications .plugin-button.active").each ->
      active_notifications[parseInt($(this).attr("data-id"))] = {}

    $(".plugin-options-accordion .accordion-group.active div.controls").each ->
      key = $(this).attr("data-param")
      id = parseInt($(this).attr("data-plugin-id"))
      active_plugins[id][key] = get_value_from_field($(this).find(".plugin-option-field"))

    $(".notification-options-accordion .accordion-group.active div.controls").each ->
      key = $(this).attr("data-param")
      id = parseInt($(this).attr("data-plugin-id"))
      active_notifications[id][key] = get_value_from_field($(this).find(".plugin-option-field"))

    schedules = []
    $(".schedule").each ->
      unless $(this).parent().attr("id") is "schedule-template"
        schedules.push
          date: $(this).find(".date").val()
          time: $(this).find(".time").val()
          repeat: $(this).find(".repeat").val()

    data =
      description: $("#description").val()
      plugins: active_plugins
      notifications: active_notifications
      schedules: schedules

    data


  get_value_from_field = (field) ->
    switch field[0].nodeName.toLowerCase()
      when "button"
        return $(field).hasClass("active")
      else
        return field.val()