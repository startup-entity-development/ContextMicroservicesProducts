""" testing git submodule Start the server with gevent. """

import os
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from app_email_gateway import create_app
monkey.patch_all()

os.environ.update()
server = WSGIServer(
    ("0.0.0.0", 3053),
    create_app(),
    handler_class=WebSocketHandler,
)
server.serve_forever()
