import logging, webapp2, datetime, uuid
from webapp2_extras import jinja2, sessions
from helpers import format_number
from google.appengine.api import memcache

def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.filters.update({
        'formatnumber': format_number,
    })
    return j

class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.session_identifier = 'tbds'
        self.session_id = None
        self.init_session()

    def init_session(self):
        session_id = self.request.cookies.get(self.session_identifier)
        if not session_id:
            session_id = uuid.uuid4().hex
            self.response.headers.add_header('Set-Cookie', '%s=%s; path=/' % (self.session_identifier, session_id))
 
        self.session_id = session_id
 
    def set_session_var(self, name, value):
        memkey = '%s-%s' % (self.session_id, name)
        memcache.set(memkey, value, 86400)
 
    def get_session_var(self, name):
        memkey = '%s-%s' % (self.session_id, name)
        return memcache.get(memkey)

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response) 
    
    webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app, factory=jinja2_factory)

    def render_template(self, filename, **template_args):
        items = {
            'url': self.request.path,
        }
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(self.jinja2.render_template(filename, args=items, **template_args))

