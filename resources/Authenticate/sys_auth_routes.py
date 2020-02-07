# ~/mysql-flask-connector/resources/Authenticate/sys_auth_routes.py

from .Auth import AuthBackend

def sys_auth_initialize_routes(api):
    api.add_resource(AuthBackend, '/api/v1/login')