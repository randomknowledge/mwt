$ ->
  if window.view_name == 'testruns'
    new Testruns()
  else if window.view_name == 'tests'
    new Tests()
  else if window.view_name == 'add_test'
    new Addtest()