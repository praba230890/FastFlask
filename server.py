from main import FastFlask, run_server, Response


app = FastFlask()

@app.route("/")
async def home(response: Response):
    response.headers[b"X-Custom-Header"] = b"Yeezy"
    return {3:30}

run_server(app)