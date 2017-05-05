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
# Update
###############################################################################
class CommentUpdateForm(flask_wtf.FlaskForm):
  content = wtforms.TextAreaField(
    model.Comment.content._verbose_name,
    [wtforms.validators.required()],
    filters=[util.strip_filter],
  )
  post_key = wtforms.SelectField(
    model.Comment.post_key._verbose_name,
    [wtforms.validators.required()],
    choices=[],
  )


@app.route('/comment/create/', methods=['GET', 'POST'])
@app.route('/comment/<int:comment_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def comment_update(comment_id=0):
  if comment_id:
    comment_db = model.Comment.get_by_id(comment_id)
  else:
    comment_db = model.Comment(user_key=auth.current_user_key())

  if not comment_db or comment_db.user_key != auth.current_user_key():
    flask.abort(404)

  form = CommentUpdateForm(obj=comment_db)

  user_dbs, user_cursor = model.User.get_dbs(limit=-1)
  post_dbs, post_cursor = model.Post.get_dbs(limit=-1)
  form.post_key.choices = [(c.key.urlsafe(), c.title) for c in post_dbs]
  if flask.request.method == 'GET' and not form.errors:
    form.post_key.data = comment_db.post_key.urlsafe() if comment_db.post_key else None

  if form.validate_on_submit():
    form.post_key.data = ndb.Key(urlsafe=form.post_key.data) if form.post_key.data else None
    form.populate_obj(comment_db)
    comment_db.put()
    return flask.redirect(flask.url_for('comment_view', comment_id=comment_db.key.id()))

  return flask.render_template(
    'comment/comment_update.html',
    title=comment_db.content if comment_id else 'New Comment',
    html_class='comment-update',
    form=form,
    comment_db=comment_db,
  )


###############################################################################
# List
###############################################################################
@app.route('/comment/')
def comment_list():
  comment_dbs, comment_cursor = model.Comment.get_dbs()
  return flask.render_template(
    'comment/comment_list.html',
    html_class='comment-list',
    title='Comment List',
    comment_dbs=comment_dbs,
    next_url=util.generate_next_url(comment_cursor),
    api_url=flask.url_for('api.comment.list'),
  )


###############################################################################
# View
###############################################################################
@app.route('/comment/<int:comment_id>/')
def comment_view(comment_id):
  comment_db = model.Comment.get_by_id(comment_id)
  if not comment_db:
    flask.abort(404)

  return flask.render_template(
    'comment/comment_view.html',
    html_class='comment-view',
    title=comment_db.content,
    comment_db=comment_db,
    api_url=flask.url_for('api.comment', comment_key=comment_db.key.urlsafe() if comment_db.key else ''),
  )


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/comment/')
@auth.admin_required
def admin_comment_list():
  comment_dbs, comment_cursor = model.Comment.get_dbs(
    order=util.param('order') or '-modified',
  )
  return flask.render_template(
    'comment/admin_comment_list.html',
    html_class='admin-comment-list',
    title='Comment List',
    comment_dbs=comment_dbs,
    next_url=util.generate_next_url(comment_cursor),
    api_url=flask.url_for('api.admin.comment.list'),
  )


###############################################################################
# Admin Update
###############################################################################
class CommentUpdateAdminForm(CommentUpdateForm):
  pass


@app.route('/admin/comment/create/', methods=['GET', 'POST'])
@app.route('/admin/comment/<int:comment_id>/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_comment_update(comment_id=0):
  if comment_id:
    comment_db = model.Comment.get_by_id(comment_id)
  else:
    comment_db = model.Comment(user_key=auth.current_user_key())

  if not comment_db:
    flask.abort(404)

  form = CommentUpdateAdminForm(obj=comment_db)

  user_dbs, user_cursor = model.User.get_dbs(limit=-1)
  post_dbs, post_cursor = model.Post.get_dbs(limit=-1)
  form.post_key.choices = [(c.key.urlsafe(), c.title) for c in post_dbs]
  if flask.request.method == 'GET' and not form.errors:
    form.post_key.data = comment_db.post_key.urlsafe() if comment_db.post_key else None

  if form.validate_on_submit():
    form.post_key.data = ndb.Key(urlsafe=form.post_key.data) if form.post_key.data else None
    form.populate_obj(comment_db)
    comment_db.put()
    return flask.redirect(flask.url_for('admin_comment_list', order='-modified'))

  return flask.render_template(
    'comment/admin_comment_update.html',
    title=comment_db.content,
    html_class='admin-comment-update',
    form=form,
    comment_db=comment_db,
    back_url_for='admin_comment_list',
    api_url=flask.url_for('api.admin.comment', comment_key=comment_db.key.urlsafe() if comment_db.key else ''),
  )


###############################################################################
# Admin Delete
###############################################################################
@app.route('/admin/comment/<int:comment_id>/delete/', methods=['POST'])
@auth.admin_required
def admin_comment_delete(comment_id):
  comment_db = model.Comment.get_by_id(comment_id)
  comment_db.key.delete()
  flask.flash('Comment deleted.', category='success')
  return flask.redirect(flask.url_for('admin_comment_list'))
