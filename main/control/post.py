# coding: utf-8

from google.appengine.ext import ndb
import flask
import flask_wtf
import wtforms

import auth
import model
import util

from main import app


###############################################################################
# Update
###############################################################################
class PostUpdateForm(flask_wtf.FlaskForm):
  title = wtforms.StringField(
    model.Post.title._verbose_name,
    [wtforms.validators.required(), wtforms.validators.length(max=500)],
    filters=[util.strip_filter],
  )
  language_key = wtforms.SelectField(
    model.Post.language_key._verbose_name,
    [wtforms.validators.required()],
    choices=[],
  )
  variant_a = wtforms.TextAreaField(
    model.Post.variant_a._verbose_name,
    [wtforms.validators.required()],
    filters=[util.strip_filter],
  )
  variant_b = wtforms.TextAreaField(
    model.Post.variant_b._verbose_name,
    [wtforms.validators.required()],
    filters=[util.strip_filter],
  )


@app.route('/post/create/', methods=['GET', 'POST'])
@app.route('/post/<int:post_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def post_update(post_id=0):
  if post_id:
    post_db = model.Post.get_by_id(post_id)
  else:
    post_db = model.Post(user_key=auth.current_user_key())

  if not post_db or post_db.user_key != auth.current_user_key():
    flask.abort(404)

  form = PostUpdateForm(obj=post_db)

  language_dbs, language_cursor = model.Language.get_dbs(limit=-1)
  user_dbs, user_cursor = model.User.get_dbs(limit=-1)
  form.language_key.choices = [(c.key.urlsafe(), c.name) for c in language_dbs]
  if flask.request.method == 'GET' and not form.errors:
    form.language_key.data = post_db.language_key.urlsafe() if post_db.language_key else None

  if form.validate_on_submit():
    form.language_key.data = ndb.Key(urlsafe=form.language_key.data) if form.language_key.data else None
    form.populate_obj(post_db)
    post_db.put()
    return flask.redirect(flask.url_for('post_view', post_id=post_db.key.id()))

  return flask.render_template(
    'post/post_update.html',
    title=post_db.title if post_id else 'Add Code Snippets',
    html_class='post-update',
    form=form,
    post_db=post_db,
  )


###############################################################################
# View
###############################################################################
@app.route('/post/<int:post_id>/')
def post_view(post_id):
  post_db = model.Post.get_by_id(post_id)
  if not post_db:
    flask.abort(404)

  vote_dbs, vote_cursor = model.Vote.get_dbs(
    limit=-1,
    ancestor=post_db.key,
    order='variant',
  )
  votes_a = 0
  for vote_db in vote_dbs:
    if vote_db.variant == 'a':
      votes_a += 1
      continue
    break
  votes_b = len(vote_dbs) - votes_a

  # my own votes, could be done better
  user_key = auth.current_user_key()
  vote_db = None
  if user_key:
    vote_db = model.Vote.query(model.Vote.user_key == user_key, ancestor=post_db.key).get()

  # Update total votes:
  if votes_a != post_db.votes_a or votes_b != post_db.votes_b:
    post_db.votes_a = votes_a
    post_db.votes_b = votes_b
    post_db.put()

  return flask.render_template(
    'post/post_view.html',
    html_class='post-view',
    title=post_db.title,
    vote_dbs=vote_dbs,
    vote_db=vote_db,
    votes_a=votes_a,
    votes_b=votes_b,
    post_db=post_db,
    api_url=flask.url_for('api.post', post_key=post_db.key.urlsafe() if post_db.key else ''),
  )


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/post/')
@auth.admin_required
def admin_post_list():
  post_dbs, post_cursor = model.Post.get_dbs(
    order=util.param('order') or '-modified',
  )
  return flask.render_template(
    'post/admin_post_list.html',
    html_class='admin-post-list',
    title='Post List',
    post_dbs=post_dbs,
    next_url=util.generate_next_url(post_cursor),
    api_url=flask.url_for('api.admin.post.list'),
  )


###############################################################################
# Admin Update
###############################################################################
class PostUpdateAdminForm(PostUpdateForm):
  pass


@app.route('/admin/post/create/', methods=['GET', 'POST'])
@app.route('/admin/post/<int:post_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_post_update(post_id=0):
  if post_id:
    post_db = model.Post.get_by_id(post_id)
  else:
    post_db = model.Post(user_key=auth.current_user_key())

  if not post_db:
    flask.abort(404)

  form = PostUpdateAdminForm(obj=post_db)

  language_dbs, language_cursor = model.Language.get_dbs(limit=-1)
  user_dbs, user_cursor = model.User.get_dbs(limit=-1)
  form.language_key.choices = [(c.key.urlsafe(), c.name) for c in language_dbs]
  if flask.request.method == 'GET' and not form.errors:
    form.language_key.data = post_db.language_key.urlsafe() if post_db.language_key else None

  if form.validate_on_submit():
    form.language_key.data = ndb.Key(urlsafe=form.language_key.data) if form.language_key.data else None
    form.populate_obj(post_db)
    post_db.put()
    return flask.redirect(flask.url_for('admin_post_list', order='-modified'))

  return flask.render_template(
    'post/admin_post_update.html',
    title=post_db.title,
    html_class='admin-post-update',
    form=form,
    post_db=post_db,
    back_url_for='admin_post_list',
    api_url=flask.url_for('api.admin.post', post_key=post_db.key.urlsafe() if post_db.key else ''),
  )


###############################################################################
# Admin Delete
###############################################################################
@app.route('/admin/post/<int:post_id>/delete/', methods=['POST'])
@auth.admin_required
def admin_post_delete(post_id):
  post_db = model.Post.get_by_id(post_id)
  post_db.key.delete()
  flask.flash('Post deleted.', category='success')
  return flask.redirect(flask.url_for('admin_post_list'))
