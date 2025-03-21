from main import FastFlask, run_server

app = FastFlask()

@app.route("/")
async def home():
    return "Hello from FastFlask!"

run_server(app)