import socket
import time
import logging
from django.conf import settings
import os
from django.utils.decorators import decorator_from_middleware

class RequestLogMiddleware(object):
    """
    This middleware gives the ability to log all requests coming in for debugging purposes

    This code was adapted from: https://stackoverflow.com/questions/15578946/logging-requests-to-django-rest-framework
    """

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):

        if response['content-type'] == 'application/json':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        else:
            response_body = '<<<Not JSON>>>'

        log_data = {
            'user': request.user.pk,

            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),

            'request_method': request.method,
            'request_path': request.get_full_path(),
            'request_body': request.body,

            'response_status': response.status_code,
            'response_body': response_body,

            'run_time': time.time() - request.start_time,
        }

        log_file = os.path.join(settings.BASE_DIR, "log.log")
        with open(log_file, 'w+') as file:
            file.write(log_file)
        return response

class RequestLogViewMixin(object):
    """
    Allows for views to inherit the logging class
    """

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(RequestLogViewMixin, cls).as_view(*args, **kwargs)
        view = decorator_from_middleware(RequestLogMiddleware)(view)
        return view