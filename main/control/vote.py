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
@app.route('/admin/vote/')
@auth.admin_required
def admin_vote_list():
  vote_dbs, vote_cursor = model.Vote.get_dbs(
    order=util.param('order') or '-modified',
  )
  return flask.render_template(
    'vote/admin_vote_list.html',
    html_class='admin-vote-list',
    title='Vote List',
    vote_dbs=vote_dbs,
    next_url=util.generate_next_url(vote_cursor),
    api_url=flask.url_for('api.admin.vote.list'),
  )


###############################################################################
# Admin Update
###############################################################################
class VoteUpdateAdminForm(flask_wtf.FlaskForm):
  user_key = wtforms.SelectField(
    model.Vote.user_key._verbose_name,
    [wtforms.validators.required()],
    choices=[],
  )
  post_key = wtforms.SelectField(
    model.Vote.post_key._verbose_name,
    [wtforms.validators.required()],
    choices=[],
  )
  variant = wtforms.SelectField(
    model.Vote.variant._verbose_name,
    [wtforms.validators.required()],
    choices=[(v, v.title()) for v in model.Vote.variant._choices],
  )


@app.route('/admin/vote/create/', methods=['GET', 'POST'])
@app.route('/admin/vote/<int:vote_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_vote_update(vote_id=0):
  if vote_id:
    vote_db = model.Vote.get_by_id(vote_id)
  else:
    vote_db = model.Vote()

  if not vote_db:
    flask.abort(404)

  form = VoteUpdateAdminForm(obj=vote_db)

  user_dbs, user_cursor = model.User.get_dbs(limit=-1)
  post_dbs, post_cursor = model.Post.get_dbs(limit=-1)
  form.user_key.choices = [(c.key.urlsafe(), c.name) for c in user_dbs]
  form.post_key.choices = [(c.key.urlsafe(), c.title) for c in post_dbs]
  if flask.request.method == 'GET' and not form.errors:
    form.user_key.data = vote_db.user_key.urlsafe() if vote_db.user_key else None
    form.post_key.data = vote_db.post_key.urlsafe() if vote_db.post_key else None

  if form.validate_on_submit():
    form.user_key.data = ndb.Key(urlsafe=form.user_key.data) if form.user_key.data else None
    form.post_key.data = ndb.Key(urlsafe=form.post_key.data) if form.post_key.data else None
    form.populate_obj(vote_db)
    vote_db.put()
    return flask.redirect(flask.url_for('admin_vote_list', order='-modified'))

  return flask.render_template(
    'vote/admin_vote_update.html',
    title='%s' % '%sVote' % ('' if vote_id else 'New '),
    html_class='admin-vote-update',
    form=form,
    vote_db=vote_db,
    back_url_for='admin_vote_list',
    api_url=flask.url_for('api.admin.vote', vote_key=vote_db.key.urlsafe() if vote_db.key else ''),
  )


###############################################################################
# Admin Delete
###############################################################################
@app.route('/admin/vote/<int:vote_id>/delete/', methods=['POST'])
@auth.admin_required
def admin_vote_delete(vote_id):
  vote_db = model.Vote.get_by_id(vote_id)
  vote_db.key.delete()
  flask.flash('Vote deleted.', category='success')
  return flask.redirect(flask.url_for('admin_vote_list'))
