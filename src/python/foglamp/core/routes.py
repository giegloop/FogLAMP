# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END

from foglamp.core import api, api_configuration, api_scheduler, api_statistics
from foglamp.core import browser
from aiohttp import web

__author__ = "Ashish Jabble, Praveen Garg"
__copyright__ = "Copyright (c) 2017 OSIsoft, LLC"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"


def setup(app):
    # app.router.add_route('POST', '/foglamp/a-post-req', api.a_post_req, expect_handler = aiohttp.web.Request.json)
    app.router.add_route('GET', '/foglamp/ping', api.ping)

    # Configuration
    app.router.add_route('GET', '/foglamp/categories', api_configuration.get_categories)
    app.router.add_route('GET', '/foglamp/category/{category_name}', api_configuration.get_category)
    app.router.add_route('GET', '/foglamp/category/{category_name}/{config_item}', api_configuration.get_category_item)
    app.router.add_route('PUT', '/foglamp/category/{category_name}/{config_item}', api_configuration.set_configuration_item,
                         expect_handler=web.Request.json)
    app.router.add_route('DELETE', '/foglamp/category/{category_name}/{config_item}', api_configuration.set_configuration_item)

    # Scheduler
    # Scheduled_processes - As per doc
    app.router.add_route('GET', '/foglamp/scheduled/processes', api_scheduler.get_scheduled_processes)
    app.router.add_route('GET', '/foglamp/scheduled/process/{scheduled_process_name}', api_scheduler.get_scheduled_process)

    # Schedules - As per doc
    app.router.add_route('GET', '/foglamp/schedules', api_scheduler.get_schedules)
    app.router.add_route('POST', '/foglamp/schedule', api_scheduler.post_schedule)
    app.router.add_route('GET', '/foglamp/schedule/{schedule_id}', api_scheduler.get_schedule)
    app.router.add_route('GET', '/foglamp/schedule/start/{schedule_id}', api_scheduler.start_schedule)
    app.router.add_route('PUT', '/foglamp/schedule/{schedule_id}', api_scheduler.update_schedule)
    app.router.add_route('DELETE', '/foglamp/schedule/{schedule_id}', api_scheduler.delete_schedule)

    # Tasks - As per doc
    app.router.add_route('GET', '/foglamp/tasks', api_scheduler.get_tasks)
    app.router.add_route('POST', '/foglamp/task', api_scheduler.post_task)
    app.router.add_route('GET', '/foglamp/tasks/latest', api_scheduler.get_tasks_latest)
    app.router.add_route('GET', '/foglamp/tasks/running', api_scheduler.get_tasks_running)
    app.router.add_route('GET', '/foglamp/task/{task_id}', api_scheduler.get_task)
    # TODO: Find out why not DELETE/PUT a task? Cancel flag can be handled in database update.
    app.router.add_route('POST', '/foglamp/task/{task_id}/cancel', api_scheduler.cancel_task)

    browser.setup(app)

    # Statistics - As per doc
    app.router.add_route('GET', '/foglamp/statistics', api_statistics.get_statistics)
    app.router.add_route('GET', '/foglamp/statistics/history', api_statistics.get_statistics_history)

    # Audit trail - As per doc
    app.router.add_route('GET', '/foglamp/audit', api.get_audit_entries)

    # enable cors support
    # Note: pip install aiohttp_cors

    # enable_cors(app)

    # enable a live debugger (watcher) for requests, see https://github.com/aio-libs/aiohttp-debugtoolbar
    # this will neutralize error middleware
    # Note: pip install aiohttp_debugtoolbar

    # enable_debugger(app)


def enable_cors(app):
    """ implements Cross Origin Resource Sharing (CORS) support """
    import aiohttp_cors

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)


def enable_debugger(app):
    """ provides a debug toolbar for server requests """
    import aiohttp_debugtoolbar

    # dev mode only
    # this will be served at API_SERVER_URL/_debugtoolbar
    aiohttp_debugtoolbar.setup(app)

