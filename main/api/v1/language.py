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


@api_v1.resource('/language/', endpoint='api.language.list')
class LanguageListAPI(flask_restful.Resource):
  def get(self):
    language_dbs, language_cursor = model.Language.get_dbs()
    return helpers.make_response(language_dbs, model.Language.FIELDS, language_cursor)


@api_v1.resource('/language/<string:language_key>/', endpoint='api.language')
class LanguageAPI(flask_restful.Resource):
  def get(self, language_key):
    language_db = ndb.Key(urlsafe=language_key).get()
    if not language_db:
      helpers.make_not_found_exception('Language %s not found' % language_key)
    return helpers.make_response(language_db, model.Language.FIELDS)


###############################################################################
# Admin
###############################################################################
@api_v1.resource('/admin/language/', endpoint='api.admin.language.list')
class AdminLanguageListAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self):
    language_keys = util.param('language_keys', list)
    if language_keys:
      language_db_keys = [ndb.Key(urlsafe=k) for k in language_keys]
      language_dbs = ndb.get_multi(language_db_keys)
      return helpers.make_response(language_dbs, model.language.FIELDS)

    language_dbs, language_cursor = model.Language.get_dbs()
    return helpers.make_response(language_dbs, model.Language.FIELDS, language_cursor)

  @auth.admin_required
  def delete(self):
    language_keys = util.param('language_keys', list)
    if not language_keys:
      helpers.make_not_found_exception('Language(s) %s not found' % language_keys)
    language_db_keys = [ndb.Key(urlsafe=k) for k in language_keys]
    ndb.delete_multi(language_db_keys)
    return flask.jsonify({
      'result': language_keys,
      'status': 'success',
    })


@api_v1.resource('/admin/language/<string:language_key>/', endpoint='api.admin.language')
class AdminLanguageAPI(flask_restful.Resource):
  @auth.admin_required
  def get(self, language_key):
    language_db = ndb.Key(urlsafe=language_key).get()
    if not language_db:
      helpers.make_not_found_exception('Language %s not found' % language_key)
    return helpers.make_response(language_db, model.Language.FIELDS)

  @auth.admin_required
  def delete(self, language_key):
    language_db = ndb.Key(urlsafe=language_key).get()
    if not language_db:
      helpers.make_not_found_exception('Language %s not found' % language_key)
    language_db.key.delete()
    return helpers.make_response(language_db, model.Language.FIELDS)
