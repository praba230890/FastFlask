from fast_flask import FastFlask, run_server, Response
from fast_flask import request
from fast_flask.middleware import logging_middleware, auth_middleware, header_middleware

app = FastFlask()

app.add_middleware(logging_middleware)
app.add_middleware(auth_middleware)
app.add_middleware(header_middleware)

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

# more complex endpoint features
@app.route("/post_data", methods=('POST'))
async def post_data(response: Response):
    print(request.method)
    print(request.query_params)
    print("cookies in server route - ", request.cookies)
    response.body = b"Data Posted"
    return response

# advanced route with multiple path parameters
@app.route("/users/{user_id}/posts/{post_id}", methods=('GET'))
async def user_post(response: Response, user_id: int, post_id: int):
    print(request.method)
    print(request.query_params)
    print("user_id in server route - ", user_id)
    print("post_id in server route - ", post_id)
    return {"user_id": user_id, "post_id": post_id}

run_server(app)
