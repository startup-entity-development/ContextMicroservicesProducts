from gevent import monkey
monkey.patch_all()
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from app_pricing_gateway import app
import os

os.environ.update()
server = WSGIServer( ("0.0.0.0", 3054),  app, handler_class=WebSocketHandler,)
server.serve_forever()
