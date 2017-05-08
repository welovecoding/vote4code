# coding: utf-8

import flask

import config
import model
import util

from main import app


###############################################################################
# Welcome
###############################################################################
@app.route('/')
def welcome():
  post_dbs, post_cursor = model.Post.get_dbs()
  return flask.render_template(
    'welcome.html',
    html_class='welcome',
    post_dbs=post_dbs,
    next_url=util.generate_next_url(post_cursor),
    api_url=flask.url_for('api.post.list'),
  )


###############################################################################
# Sitemap stuff
###############################################################################
@app.route('/sitemap.xml')
def sitemap():
  response = flask.make_response(flask.render_template(
    'sitemap.xml',
    lastmod=config.CURRENT_VERSION_DATE.strftime('%Y-%m-%d'),
  ))
  response.headers['Content-Type'] = 'application/xml'
  return response


###############################################################################
# Warmup request
###############################################################################
@app.route('/_ah/warmup')
def warmup():
  # TODO: put your warmup code here
  return 'success'
