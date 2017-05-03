# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Language(model.Base):
  name = ndb.StringProperty(required=True)

  def get_post_dbs(self, **kwargs):
    return model.Post.get_dbs(language_key=self.key, **kwargs)

  @classmethod
  def _pre_delete_hook(cls, key):
    language_db = key.get()
    post_keys = language_db.get_post_dbs(keys_only=True, limit=-1)[0]
    ndb.delete_multi(post_keys)

  FIELDS = {
    'name': fields.String,
  }

  FIELDS.update(model.Base.FIELDS)
