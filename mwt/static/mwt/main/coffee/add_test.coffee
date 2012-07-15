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

    $("#main_form").submit (event) =>
      event.preventDefault()
      @submitForm()

    $("#add-schedule-button").click (event) =>
      event.preventDefault()
      schedule_id++
      @addSchedule schedule_id

  addSchedule: (id, paused=false, repeat='no') ->
    tpl = $("#schedule-template").html().replace(/\[id\]/g, id)
    $("#add-schedule-button").after $(tpl)
    ele = $("##{$(tpl).attr 'id'}")

    $(".close-schedule").unbind "click"
    $(".close-schedule").click (event) ->
      event.preventDefault()
      $(event.currentTarget).parent().remove()

    $(".button-play-pause").click (event) ->
      event.preventDefault()

    ele.find("select[name=repeat] option[value=#{repeat}]").attr 'selected', 'selected'
    ele.find(".button-play-pause").toggleClass 'active', paused

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


  submitForm: =>
    url = Utils.getAjaxUrl()
    console.log @collect_form_data()
    $.ajax
      url: url + "&data=" + JSON.stringify(@collect_form_data())
      type: "GET"
      dataType: "json"
      processdata: false
      success: (data, textStatus, jqXHR) ->
        console.log data

      error: (jqXHR, textStatus, errorThrown) ->
        console.log jqXHR, textStatus, errorThrown


  collect_form_data: ->
    active_plugins = []
    active_notifications = []
    $("#plugins .plugin-button.active").each (idx, ele) =>
      pid = parseInt $(ele).attr("data-id")
      plugin = {'id': pid, 'options': []}
      $(".plugin-options-accordion .accordion-group.active div.controls[data-plugin-id=#{pid}]").each (idx, ele) =>
        option_id = $(ele).attr('data-option-id')
        key = $(ele).attr("data-param")
        value = @get_value_from_field($(ele).find(".plugin-option-field"))
        plugin.options.push { 'id': option_id, 'key': key, 'value': value }
      active_plugins.push plugin

    $("#notifications .plugin-button.active").each (idx, ele) =>
      #active_notifications[parseInt($(this).attr("data-id"))] = {}
      pid = parseInt $(ele).attr("data-id")
      plugin = {'id': pid, 'options': []}
      $(".notification-options-accordion .accordion-group.active div.controls[data-plugin-id=#{pid}]").each (idx, ele) =>
        option_id = $(ele).attr('data-option-id')
        key = $(ele).attr("data-param")
        value = @get_value_from_field($(ele).find(".plugin-option-field"))
        plugin.options.push { 'id': option_id, 'key': key, 'value': value }
      active_notifications.push plugin

    schedules = []
    $(".schedule").each ->
      unless $(this).parent().attr("id") is "schedule-template"
        schedules.push
          id: $(this).attr 'data-schedule-id'
          paused: $(this).find('.button-play-pause').hasClass('active')
          date: $(this).find(".date").val()
          time: $(this).find(".time").val()
          repeat: $(this).find(".repeat").val()

    data =
      description: $("#description").val()
      plugins: active_plugins
      notifications: active_notifications
      schedules: schedules

    data


  get_value_from_field: (field) ->
    switch field[0].nodeName.toLowerCase()
      when "button"
        return $(field).hasClass("active")
      else
        return field.val()