# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb
import flask
import flask_restful

from api import helpers
import auth
import model
import util

from main import api_v1


@api_v1.resource('/post/', endpoint='api.post.list')
class PostListAPI(flask_restful.Resource):
  def get(self):
    post_dbs, post_cursor = model.Post.get_dbs()
    return helpers.make_response(post_dbs, model.Post.FIELDS, post_cursor)


@api_v1.resource('/post/<string:post_key>/', endpoint='api.post')
class PostAPI(flask_restful.Resource):
  def get(self, post_key):
    post_db = ndb.Key(urlsafe=post_key).get()
    if not post_db:
      helpers.make_not_found_exception('Post %s not found' % post_key)
    return helpers.make_response(post_db, model.Post.FIELDS)


###############################################################################
# Admin
###############################################################################
@api_v1.resource('/admin/post/', endpoint='api.admin.post.list')
class AdminPostListAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self):
    post_keys = util.param('post_keys', list)
    if post_keys:
      post_db_keys = [ndb.Key(urlsafe=k) for k in post_keys]
      post_dbs = ndb.get_multi(post_db_keys)
      return helpers.make_response(post_dbs, model.post.FIELDS)

    post_dbs, post_cursor = model.Post.get_dbs()
    return helpers.make_response(post_dbs, model.Post.FIELDS, post_cursor)

  @auth.admin_required
  def delete(self):
    post_keys = util.param('post_keys', list)
    if not post_keys:
      helpers.make_not_found_exception('Post(s) %s not found' % post_keys)
    post_db_keys = [ndb.Key(urlsafe=k) for k in post_keys]
    ndb.delete_multi(post_db_keys)
    return flask.jsonify({
      'result': post_keys,
      'status': 'success',
    })


@api_v1.resource('/admin/post/<string:post_key>/', endpoint='api.admin.post')
class AdminPostAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self, post_key):
    post_db = ndb.Key(urlsafe=post_key).get()
    if not post_db:
      helpers.make_not_found_exception('Post %s not found' % post_key)
    return helpers.make_response(post_db, model.Post.FIELDS)

  @auth.admin_required
  def delete(self, post_key):
    post_db = ndb.Key(urlsafe=post_key).get()
    if not post_db:
      helpers.make_not_found_exception('Post %s not found' % post_key)
    post_db.key.delete()
    return helpers.make_response(post_db, model.Post.FIELDS)
