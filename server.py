from fast_flask import FastFlask, run_server, Response
from fast_flask import request


app = FastFlask()

@app.route("/", methods=('GET'))
async def home(response: Response):
    response.headers[b"X-Custom-Header"] = b"Yeezy"
    print(request.method)
    print(request.query_params)
    print("cookies in server route - ", request.cookies)
    response.cookies["MAD"] = "Man"
    response.body = {3:30}
    # return response
    return {3:40}

@app.route("/users/{id}", methods=('GET'))
async def user(response: Response, id: int):
    print(request.method)
    print(request.query_params)
    print("id in server route - ", id)
    return {"id": 100}

run_server(app)
