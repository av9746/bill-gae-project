#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")


class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")


class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contactUs.html")

    def post(self):
        error = False
        alerts = []
        sent_message = {}

        name = self.request.get("name")
        email = self.request.get("email")
        subject = self.request.get("subject")
        message = self.request.get("message")

        if name == "":
            error = True
            alerts.append("Name missing")

        if email == "":
            error = True
            alerts.append("email missing")

        if subject == "":
            error = True
            alerts.append("subject missing")

        if message == "":
            error = True
            alerts.append("message missing")

        if error == False:
            sent_message = {"name": name, "email": email, "subject": subject, "message": message}

        params = {"sent_message": sent_message, "error": error, "alerts": alerts}

        self.render_template("contactUs.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/contact', ContactHandler)
], debug=True)
