from gevent import monkey
#monkey.patch_all()
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from app_auth_gateway import app
import os

os.environ.update()
server = WSGIServer(("0.0.0.0", 3050), app, handler_class=WebSocketHandler)
server.serve_forever()
