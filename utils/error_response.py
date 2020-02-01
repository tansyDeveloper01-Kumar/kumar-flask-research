def error_response(**kwargs):
    return {
        'error': {
            'message': kwargs['message'],
            'type': kwargs['type'],
            'code': kwargs['code'],
            'fbtrace_id': kwargs['fbtrace_id']
        }
    }