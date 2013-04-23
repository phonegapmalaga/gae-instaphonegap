from google.appengine.ext import db


class Upload(db.Model):

    file = db.BlobProperty()
    caption = db.StringProperty()