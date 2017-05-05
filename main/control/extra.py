# coding: utf-8

# This file to be integrated somewhere else eventually :)

import flask

import auth
import model

from main import app


@app.route('/post/<int:post_id>/vote/<variant>/', methods=['GET', 'POST'])
@auth.login_required
def post_vote(post_id, variant):
  post_db = model.Post.get_by_id(post_id)
  if not post_db or variant not in ['a', 'b']:
    flask.abort(404)
  user_db = auth.current_user_db()
  code = '%s-%s' % (post_db.key.id(), user_db.key.id())
  vote_db = model.Vote.get_or_insert(
    code,
    parent=post_db.key,
    user_key=user_db.key,
    post_key=post_db.key,
    variant=variant,
  )
  vote_db.variant = variant
  vote_db.put()

  return flask.redirect(flask.url_for('post_view', post_id=post_db.key.id()))
