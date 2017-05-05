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
  votes_a = ndb.IntegerProperty(default=0)
  votes_b = ndb.IntegerProperty(default=0)

  @ndb.ComputedProperty
  def votes(self):
    return self.votes_a + self.votes_b

  @ndb.ComputedProperty
  def votes_a_percentage(self):
    if self.votes > 0:
      return 1.0 * self.votes_a / self.votes
    return 0

  @ndb.ComputedProperty
  def votes_b_percentage(self):
    if self.votes > 0:
      return 1.0 * self.votes_b / self.votes
    return 0

  @classmethod
  def get_dbs(cls, order=None, **kwargs):
    return super(Post, cls).get_dbs(
      order=order or util.param('order') or '-created',
      **kwargs
    )

  def get_vote_dbs(self, **kwargs):
    return model.Vote.get_dbs(post_key=self.key, **kwargs)

  def get_comment_dbs(self, **kwargs):
    return model.Comment.get_dbs(ancestor=self.key, **kwargs)

  @classmethod
  def _pre_delete_hook(cls, key):
    post_db = key.get()
    vote_keys = post_db.get_vote_dbs(keys_only=True, limit=-1)[0]
    comment_keys = post_db.get_comment_dbs(keys_only=True, limit=-1)[0]
    ndb.delete_multi(vote_keys + comment_keys)

  FIELDS = {
    'title': fields.String,
    'language_key': fields.Key,
    'variant_a': fields.String,
    'variant_b': fields.String,
    'user_key': fields.Key,
    'votes_a': fields.Integer,
    'votes_b': fields.Integer,
  }

  FIELDS.update(model.Base.FIELDS)
