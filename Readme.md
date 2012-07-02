# Disclaimer

## This software is pre-alpha. Use at your own risk!

____

**`MWT` or multipurpose website testing is a [Django](https://www.djangoproject.com/) app
for managing website tests (like "is site up?").
New tests are can be added as plugins.**

____
[![Build Status](https://secure.travis-ci.org/randomknowledge/mwt.png?branch=master)](http://travis-ci.org/randomknowledge/mwt)

## Requirements
#### Main
* [Django 1.4](https://www.djangoproject.com/)
* [South](http://south.aeracode.org/)
* [pytz](http://pypi.python.org/pypi/pytz/)
* [html5lib](http://code.google.com/p/html5lib/)
* [lxml](https://github.com/lxml/lxml)
* [RQ](https://github.com/nvie/rq/)

#### For plugins
* [PhantomJS](http://phantomjs.org/) and [CasperJS](http://casperjs.org/) (For google search index plugin)


## Installation

Download source and install package using pip:

```console
$ pip install -e git+https://github.com/randomknowledge/mwt.git#egg=mwt
```


## Configuration

Add this to your project's `settings.py` and add `mwt` to INSTALLED_APPS.
Those are also the default settings:

```python
PHANTOM_JS_BIN = '/path/to/bin/phantomjs'
CASPER_JS_BIN = '/path/to/bin/casperjs'

REDIS_SETTINGS = {
    'connection': {
        'db': 0,
        'host': 'localhost',
        'port': 6379,
        },
    'eager': False,  # If True, Tasks are not queued, but executed directly. Use for testing purposes only!
    'queue_prefix': 'mwt:'  # MWT will prefix all (RQ-)Queues with this prefix.
}

MWT_SETTINGS = {
    'url': 'http://localhost:8000',  # Base URL of MWT
    'name': 'localhost',  # The human-readable name of your MWT instance
    'email_from': 'MWT Server <noreply@localhost>',  # From-Address for all e-mails
}
```


## Running `MWT`

`MWT` uses two (rq-)queues: `mwt:tasks` and `mwt:notifications`
(Note: if you set the `queue_prefix` different from `mwt:` in
your `settings.py`, the queue names change accordingly.)

Inside your [virtualenv](http://pypi.python.org/pypi/virtualenv/) let your
rq-workers listen to the mwt-queues. It makes sense to at least start two
workers, One for `tasks` and one for `notifications`. But of course you can
also have only one worker for both or as many workers as you want for any of each:

Make sure to let the workers know the location of your django settings. e.g.:

```console
(virtualenv)$ export DJANGO_SETTINGS_MODULE="path.to.settings"
```

Listen on `tasks` queue

```console
(virtualenv)$ rqworker mwt:tasks
```

Listen on `notifications` queue

```console
(virtualenv)$ rqworker mwt:notifications
```

Start the `MWT` taskrunner either in burst- or deamon-mode. It will regularly
check for pending tasks and push them to the queues.

In `burst-mode` the taskrunner will run once and exit.
Use this for testing or in cron-jobs.

```console
(virtualenv)$ python manage.py taskrunner burst
```

In `deamon-mode` the taskrunner will run until killed.
(Note that the taskrunner doesn't deamonize itself.
Use [supervisor](http://supervisord.org/) or similar for this.)

```console
(virtualenv)$ python manage.py taskrunner deamon
```


## Using `MWT`

Log in to you django admin and start by adding `tests`.
Each `test` can run several `plugins`, `notifications` and `run schedules`.
When a test is started (by the `taskrunner` it will first run all it's `plugins`
and after that run it's `notifications`.


## TODO

This software is far from finished and needs a lot of optimization. Actually too much to list...