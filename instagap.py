from google.appengine.ext import db
import webapp2
import jinja2
import re
import base64
from model import Upload

JINJA_ENV = jinja2.Environment(
    loader = jinja2.FileSystemLoader('templates')
)


class HomePageHandler(webapp2.RequestHandler):

    def get(self):

        uploads = Upload.all().fetch(100)

        template = JINJA_ENV.get_template("index.html")
        template_values = {
            'uploads': uploads
        }
        self.response.write(template.render(template_values))

class UploadHandler(webapp2.RequestHandler):

    def post(self):

        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        file_data = self.request.get("file")
        imgb64 = dataUrlPattern.match(file_data).group(2)

        caption = self.request.get("caption")

        upload = Upload()
        upload.file = db.Blob(base64.b64decode(imgb64))
        upload.caption = caption
        upload.put()

        self.redirect("/")

class ImageHandler(webapp2.RequestHandler):

    def get(self):

        img_id = self.request.get("img_id")
        upload = db.get(img_id)
        self.response.write(upload.file)
        self.response.headers['Content-Type'] = 'image/jpeg'

patterns = [
    ('/', HomePageHandler),
    ('/upload', UploadHandler),
    ('/img', ImageHandler)
]

app = webapp2.WSGIApplication(patterns, debug=True)