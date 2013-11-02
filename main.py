import cgi
import jinja2
import json
import os
import urllib
import webapp2

import theFunctions as func
from google.appengine.api import users
from google.appengine.ext import ndb, db


# Add libs folder path to get 3rd party libs not in GAE

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class WordLink(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    words = ndb.JsonProperty()
    link = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        cur_user = users.get_current_user()
        if cur_user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        try: nickname = cur_user.nickname()
        except: nickname = ''
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'cur_user' : nickname
        }

        #RENDER FORM TO ENTER URLS/QUERIES IN

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))



class SaveLinks(webapp2.RequestHandler):
    def post(self):
        term = self.request.get('content')
        valid_input = func.valid_input(term)
        # self.response.write("%s is a valid term: %s <br>" % (term, valid_input))
        is_url = func.is_url(term)
        if is_url:
            # Write to see what crawl_page returns 
            #self.response.write(func.crawl_page(term))
            crawl = func.crawl_page(term)
            if crawl:
                url_term = WordLink()
                url_term.author = users.get_current_user()
                url_term.words = json.dumps(list(crawl))
                url_term.link = term

                url_term.put()
                self.response.write("%s is saved successfully!" % term)
            else:
                self.response.write("The URL %s was not searchable. \
                    Try again!" % term)

        else: # It's a Query
            url_query = WordLink.query()
            url_words = url_query.filter(ndb.GenericProperty('author') == users.get_current_user())  #fetch()
            #self.response.write("%s <br><br>" % term)
            
            self.response.write("%s <br>" % term)
            for entry in url_words:
                for word in json.loads(entry.words):
                    if word == str(term.lower().strip()):
                        self.response.write("<a href=%s>%s</a><br>" % (entry.link,entry.link))
                        break
            



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/savelinks', SaveLinks),
], debug=True)
