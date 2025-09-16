# need to move middleware to its own file
# class MiddlewareManager:
# 	def __init__(self):
# 		self._middlewares = []

# 	def add_middleware(self, middleware_func):
# 		"""
# 		Register a middleware function.
# 		Middleware should accept (request, response, next_func)
# 		"""
# 		self._middlewares.append(middleware_func)

# 	def execute(self, request, response):
# 		"""
# 		Execute all middleware in order.
# 		Each middleware receives (request, response, next_func).
# 		"""
# 		def _run(index):
# 			if index < len(self._middlewares):
# 				def next_func():
# 					_run(index + 1)
# 				self._middlewares[index](request, response, next_func)
# 			# else: end of chain
# 		_run(0)

async def logging_middleware(scope, response, call_next):
    print(f"[LOG] {scope['method']} {scope['path']}")
    return await call_next()

async def auth_middleware(scope, response, call_next):
    headers = dict(scope["headers"])
    token = headers.get(b"authorization", None)
    if token != b"Bearer secret":
        response.status = 401
        response.body = b"Unauthorized"
        return response
    return await call_next()

async def header_middleware(scope, response, call_next):
    resp = await call_next()
    resp.headers[b"X-Powered-By"] = b"FastFlask"
    return resp