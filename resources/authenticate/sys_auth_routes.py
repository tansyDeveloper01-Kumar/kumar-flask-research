# ~/mysql-flask-connector/resources/authenticate/sys_auth_routes.py

from .auth import clsLogin

def fn_sys_auth_initialize_routes(api):
    api.add_resource(clsLogin, '/api/v1/login')