from main import FastFlask, run_server, Response, request


app = FastFlask()

@app.route("/", methods=('GET'))
async def home(response: Response):
    response.headers[b"X-Custom-Header"] = b"Yeezy"
    print(request.method)
    return {3:30}


run_server(app)