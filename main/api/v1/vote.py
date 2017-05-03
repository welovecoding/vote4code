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


@api_v1.resource('/vote/', endpoint='api.vote.list')
class VoteListAPI(flask_restful.Resource):
  def get(self):
    vote_dbs, vote_cursor = model.Vote.get_dbs()
    return helpers.make_response(vote_dbs, model.Vote.FIELDS, vote_cursor)


@api_v1.resource('/vote/<string:vote_key>/', endpoint='api.vote')
class VoteAPI(flask_restful.Resource):
  def get(self, vote_key):
    vote_db = ndb.Key(urlsafe=vote_key).get()
    if not vote_db:
      helpers.make_not_found_exception('Vote %s not found' % vote_key)
    return helpers.make_response(vote_db, model.Vote.FIELDS)


###############################################################################
# Admin
###############################################################################
@api_v1.resource('/admin/vote/', endpoint='api.admin.vote.list')
class AdminVoteListAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self):
    vote_keys = util.param('vote_keys', list)
    if vote_keys:
      vote_db_keys = [ndb.Key(urlsafe=k) for k in vote_keys]
      vote_dbs = ndb.get_multi(vote_db_keys)
      return helpers.make_response(vote_dbs, model.vote.FIELDS)

    vote_dbs, vote_cursor = model.Vote.get_dbs()
    return helpers.make_response(vote_dbs, model.Vote.FIELDS, vote_cursor)

  @auth.admin_required
  def delete(self):
    vote_keys = util.param('vote_keys', list)
    if not vote_keys:
      helpers.make_not_found_exception('Vote(s) %s not found' % vote_keys)
    vote_db_keys = [ndb.Key(urlsafe=k) for k in vote_keys]
    ndb.delete_multi(vote_db_keys)
    return flask.jsonify({
      'result': vote_keys,
      'status': 'success',
    })


@api_v1.resource('/admin/vote/<string:vote_key>/', endpoint='api.admin.vote')
class AdminVoteAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self, vote_key):
    vote_db = ndb.Key(urlsafe=vote_key).get()
    if not vote_db:
      helpers.make_not_found_exception('Vote %s not found' % vote_key)
    return helpers.make_response(vote_db, model.Vote.FIELDS)

  @auth.admin_required
  def delete(self, vote_key):
    vote_db = ndb.Key(urlsafe=vote_key).get()
    if not vote_db:
      helpers.make_not_found_exception('Vote %s not found' % vote_key)
    vote_db.key.delete()
    return helpers.make_response(vote_db, model.Vote.FIELDS)
