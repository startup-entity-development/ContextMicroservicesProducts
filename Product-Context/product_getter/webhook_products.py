from aiohttp import web

async def webkook(request):
    print(f"webhook request: {request.json()}")
    return web.Response(text="Webhook received")

app = web.Application()
app.add_routes([web.post('/', webkook)])

web.run_app(app,port=5055)