# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Comment(model.Base):
  content = ndb.TextProperty(required=True)
  user_key = ndb.KeyProperty(kind=model.User, required=True)
  post_key = ndb.KeyProperty(kind=model.Post, required=True, verbose_name=u'Post')

  FIELDS = {
    'content': fields.String,
    'user_key': fields.Key,
    'post_key': fields.Key,
  }

  FIELDS.update(model.Base.FIELDS)
