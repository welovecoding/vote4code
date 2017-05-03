# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Post(model.Base):
  title = ndb.StringProperty(required=True)
  language_key = ndb.KeyProperty(kind=model.Language, required=True, verbose_name=u'Language')
  variant_a = ndb.TextProperty(required=True)
  variant_b = ndb.TextProperty(required=True)
  user_key = ndb.KeyProperty(kind=model.User, required=True)

  def get_vote_dbs(self, **kwargs):
    return model.Vote.get_dbs(post_key=self.key, **kwargs)

  @classmethod
  def _pre_delete_hook(cls, key):
    post_db = key.get()
    vote_keys = post_db.get_vote_dbs(keys_only=True, limit=-1)[0]
    ndb.delete_multi(vote_keys)

  FIELDS = {
    'title': fields.String,
    'language_key': fields.Key,
    'variant_a': fields.String,
    'variant_b': fields.String,
    'user_key': fields.Key,
  }

  FIELDS.update(model.Base.FIELDS)
