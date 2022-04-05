from flask_session.sessions import RedisSessionInterface, NullSessionInterface
from flask_session import Session

class CustomRedisSessionInterface(RedisSessionInterface):
    """Uses the Redis key-value store as a session backend. It extends
    the default RedisSessionInterface to include a
    regenrate session method

    .. versionadded:: 0.2
        The `use_signer` parameter was added.

    :param redis: A ``redis.Redis`` instance.
    :param key_prefix: A prefix that is added to all Redis store keys.
    :param use_signer: Whether to sign the session id cookie or not.
    :param permanent: Whether to use permanent session or not.
    """

    def __init__(self, redis, key_prefix, use_signer=False, permanent=True):
        super().__init__(redis, key_prefix, use_signer, permanent)

    def save_session(self, app, session, response):
        if len(session.keys()) == 1:
            if list(session.keys())[0] == '_permanent':
                return        
            # clears the _permanent key from session variable if it's the only key in the
            # session object. The _permanent is created automatically once a request is made
            # to the server and persists to the redis store (which is used for sever side session
            # store) and affects program logic. Only want a session to be created/persist only
            # on the creation of any custom key manually by code.
        super().save_session(app, session, response)
        

    def regenerate_session(self, session):
        """Regenerates current session with a new session id."""
        #deletes old session info from redis database
        self.redis.delete(self.key_prefix + session.sid)

        # generate new session id and mark the session as modified
        session.sid = self._generate_sid()
        session.modified = True

        #session data will be preserved on the 'session dict'
        #'save_session' will take care of updating the cookie"

    
class CustomSession(Session):
    """This class is used to add Server-side Session to one or more Flask
    applications. 
    It extends the function of the default Flask-Session 'Session' Object
    by overiding the '_get_interface' method to recognize custom session
    interfaces
    
    By default CustomSession will use :class:`NullSessionInterface`.

    .. note::

        You can not use ``CustomSession`` instance directly, what ``Session`` does
        is just change the :attr:`~flask.Flask.session_interface` attribute on
        your Flask applications.
    """
    
    def __init__(self, app=None):
        super().__init__(app)
    
    def _get_interface(self, app):
        config = app.config.copy()
        config.setdefault('SESSION_TYPE', 'null')
        config.setdefault('SESSION_PERMANENT', True)
        config.setdefault('SESSION_USE_SIGNER', False)
        config.setdefault('SESSION_KEY_PREFIX', 'session:')
        config.setdefault('SESSION_REDIS', None)
        # from pprint import pprint
        # pprint(config)
        if config['SESSION_TYPE'] == 'custom_redis':
            session_interface = CustomRedisSessionInterface(
                config['SESSION_REDIS'], config['SESSION_KEY_PREFIX'],
                config['SESSION_USE_SIGNER'], config['SESSION_PERMANENT'])
        else:
            session_interface = super()._get_interface(app)
        return session_interface