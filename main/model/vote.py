# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Vote(model.Base):
  user_key = ndb.KeyProperty(kind=model.User, required=True, verbose_name=u'User')
  post_key = ndb.KeyProperty(kind=model.Post, required=True, verbose_name=u'Post')
  variant = ndb.StringProperty(required=True, choices=['a', 'b'])

  FIELDS = {
    'user_key': fields.Key,
    'post_key': fields.Key,
    'variant': fields.String,
  }

  FIELDS.update(model.Base.FIELDS)
