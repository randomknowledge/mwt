class @Edittest extends Addtest
  constructor: (@name) ->
    super
    for task in window.test_data.tasks
      $("#plugins .plugin-button[data-id=#{task.id}]").click()
      for option in task.options
        control = $("#plugin-options-#{task.id} div[data-param=#{option.key}]")
        control.attr 'data-option-id', option.id
        obj = control.children().first()
        obj.val(option.value)

    for notification in window.test_data.notifications
      $("#notifications .plugin-button[data-id=#{notification.id}]").click()
      for option in notification.options
        control = $("#notification-options-#{notification.id} div[data-param=#{option.key}]")
        control.attr 'data-option-id', option.id
        obj = control.children().first()
        if obj.is('button')
          if option.value == 0 or option.value == "0"
            obj.toggleClass 'active', false
          else
            obj.toggleClass 'active', true
        else
          obj.val(option.value)

    for schedule in window.test_data.schedules
      @addSchedule schedule.id, schedule.paused, schedule.repeat