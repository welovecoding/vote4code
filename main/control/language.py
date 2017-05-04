# coding: utf-8

from google.appengine.ext import ndb
import flask
import flask_wtf
import wtforms

import auth
import config
import model
import util

from main import app


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/language/')
@auth.admin_required
def admin_language_list():
  language_dbs, language_cursor = model.Language.get_dbs(
    order=util.param('order') or '-modified',
  )
  return flask.render_template(
    'language/admin_language_list.html',
    html_class='admin-language-list',
    title='Language List',
    language_dbs=language_dbs,
    next_url=util.generate_next_url(language_cursor),
    api_url=flask.url_for('api.admin.language.list'),
  )


###############################################################################
# Admin Update
###############################################################################
class LanguageUpdateAdminForm(flask_wtf.FlaskForm):
  name = wtforms.StringField(
    model.Language.name._verbose_name,
    [wtforms.validators.required(), wtforms.validators.length(max=500)],
    filters=[util.strip_filter],
  )
  slug = wtforms.StringField(
    model.Language.slug._verbose_name,
    [wtforms.validators.required(), wtforms.validators.length(max=500)],
    filters=[util.strip_filter],
  )


@app.route('/admin/language/create/', methods=['GET', 'POST'])
@app.route('/admin/language/<int:language_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_language_update(language_id=0):
  if language_id:
    language_db = model.Language.get_by_id(language_id)
  else:
    language_db = model.Language()

  if not language_db:
    flask.abort(404)

  form = LanguageUpdateAdminForm(obj=language_db)

  if form.validate_on_submit():
    form.populate_obj(language_db)
    language_db.put()
    return flask.redirect(flask.url_for('admin_language_list', order='-modified'))

  return flask.render_template(
    'language/admin_language_update.html',
    title='%s' % language_db.name if language_id else 'New Language',
    html_class='admin-language-update',
    form=form,
    language_db=language_db,
    back_url_for='admin_language_list',
    api_url=flask.url_for('api.admin.language', language_key=language_db.key.urlsafe() if language_db.key else ''),
  )


###############################################################################
# Admin Delete
###############################################################################
@app.route('/admin/language/<int:language_id>/delete/', methods=['POST'])
@auth.admin_required
def admin_language_delete(language_id):
  language_db = model.Language.get_by_id(language_id)
  language_db.key.delete()
  flask.flash('Language deleted.', category='success')
  return flask.redirect(flask.url_for('admin_language_list'))
