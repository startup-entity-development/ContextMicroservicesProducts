import os
from gevent.pywsgi import WSGIServer
from gevent import monkey
#monkey.patch_all()

from geventwebsocket.handler import WebSocketHandler
from app_product_gateway import app

os.environ.update()
server = WSGIServer(
    ("0.0.0.0", 3051),app, handler_class=WebSocketHandler,)
server.serve_forever()
