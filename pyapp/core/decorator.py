import functools

def login_required(cls):
    cls.login_required = True
    return cls




def type_check(func):

    @functools.wraps(func)
    def check(*args, **kwargs):
        for name, value in kwargs.items():
            v = value
            v_name = name
            if name not in func.__annotations__:
                continue
                
            v_type = func.__annotations__[name]

            error_msg = 'Variable `' + str(v_name) + '` should be type ('
            error_msg += str(v_type) + ') but instead is type (' + str(type(v)) + ') '
            if not isinstance(v, v_type):
                raise TypeError(error_msg)

        result = func(*args, **kwargs)
        if 'return' in func.__annotations__:
            v = result
            v_name = 'return'
            v_type = func.__annotations__['return']
            error_msg = 'Variable `' + str(v_name) + '` should be type ('
            error_msg += str(v_type) + ') but instead is type (' + str(type(v)) + ')'
            if not isinstance(v, v_type):
                    raise TypeError(error_msg)
        return result

    return check