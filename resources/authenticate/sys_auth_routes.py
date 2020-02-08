# ~/mysql-flask-connector/resources/authenticate/sys_auth_routes.py

from .auth import AuthBackend

def sys_auth_initialize_routes(api):
    api.add_resource(AuthBackend, '/api/v1/login')