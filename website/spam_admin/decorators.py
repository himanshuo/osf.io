import functools
from flask import request
from framework.flask import redirect
from framework.auth.core import Auth

def must_be_spam_admin(func):
    """Require that user be spam_admin.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):


        kwargs['auth'] = Auth.from_kwargs(request.args.to_dict(), kwargs)
        # if kwargs['auth'].user.fullname=="spam_admin" and kwargs['auth'].user.emails[0]=="spam_admin@cos.com" :
        #     kwargs['auth'].user.spam_admin=True
        #     kwargs['auth'].user.save()
        if kwargs['auth'].user.spam_admin:
            return func(*args, **kwargs)
        else:
            return redirect('/login/?next={0}'.format(request.path))

    return wrapped
