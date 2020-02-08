import flask
import functools

def check_screen_permission(screen_name = ''):
    """
    check user permission for screen
    will also add current screen id to request object
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            # data = request.session.get('MENU_DATA', [])
            screen_name = flask.request.headers.get('screen_name')
            data = [1]
            screen = None
            for item in data:
                name = "products" # str(item['screen_name']).lower().replace(' ','-')
                if(name == screen_name):
                    screen = item
                    break

            if(screen is None):
                return { 'status': "Failure", "Message": "Screen name does not exist"}

            return function(request, *args, **kwargs)

        return wrapper
    return decorator

