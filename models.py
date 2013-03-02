from google.appengine.ext import ndb

class TestModel(ndb.Model):
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    searched_at = ndb.DateTimeProperty(auto_now=True)
    title = ndb.StringProperty()
    content = ndb.TextProperty()
