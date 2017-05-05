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


@api_v1.resource('/comment/', endpoint='api.comment.list')
class CommentListAPI(flask_restful.Resource):
  def get(self):
    comment_dbs, comment_cursor = model.Comment.get_dbs()
    return helpers.make_response(comment_dbs, model.Comment.FIELDS, comment_cursor)


@api_v1.resource('/comment/<string:comment_key>/', endpoint='api.comment')
class CommentAPI(flask_restful.Resource):
  def get(self, comment_key):
    comment_db = ndb.Key(urlsafe=comment_key).get()
    if not comment_db:
      helpers.make_not_found_exception('Comment %s not found' % comment_key)
    return helpers.make_response(comment_db, model.Comment.FIELDS)


###############################################################################
# Admin
###############################################################################
@api_v1.resource('/admin/comment/', endpoint='api.admin.comment.list')
class AdminCommentListAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self):
    comment_keys = util.param('comment_keys', list)
    if comment_keys:
      comment_db_keys = [ndb.Key(urlsafe=k) for k in comment_keys]
      comment_dbs = ndb.get_multi(comment_db_keys)
      return helpers.make_response(comment_dbs, model.comment.FIELDS)

    comment_dbs, comment_cursor = model.Comment.get_dbs()
    return helpers.make_response(comment_dbs, model.Comment.FIELDS, comment_cursor)

  @auth.admin_required
  def delete(self):
    comment_keys = util.param('comment_keys', list)
    if not comment_keys:
      helpers.make_not_found_exception('Comment(s) %s not found' % comment_keys)
    comment_db_keys = [ndb.Key(urlsafe=k) for k in comment_keys]
    ndb.delete_multi(comment_db_keys)
    return flask.jsonify({
      'result': comment_keys,
      'status': 'success',
    })


@api_v1.resource('/admin/comment/<string:comment_key>/', endpoint='api.admin.comment')
class AdminCommentAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self, comment_key):
    comment_db = ndb.Key(urlsafe=comment_key).get()
    if not comment_db:
      helpers.make_not_found_exception('Comment %s not found' % comment_key)
    return helpers.make_response(comment_db, model.Comment.FIELDS)

  @auth.admin_required
  def delete(self, comment_key):
    comment_db = ndb.Key(urlsafe=comment_key).get()
    if not comment_db:
      helpers.make_not_found_exception('Comment %s not found' % comment_key)
    comment_db.key.delete()
    return helpers.make_response(comment_db, model.Comment.FIELDS)
