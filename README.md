# vote4code

The vote4code website is place to upload two different versions of programming solutions to let the community vote for the best one. It's based on [**gae-init**](https://github.com/gae-init/gae-init).

## Requirements

### Python
- [Python 2.7](https://www.python.org/downloads/)
- [pip](http://docs.gae-init.appspot.com/requirement/#pip)
- [virtualenv](http://docs.gae-init.appspot.com/requirement/#virtualenv)

### Node.js
- [Node.js](https://nodejs.org/en/)
- [Gulp](http://gulpjs.com/)

### Google Cloud Platform
- [Google Cloud SDK](https://cloud.google.com/sdk/)
- [Google App Engine SDK 1.9.53 for Python](https://cloud.google.com/appengine/docs/standard/python/download)

## Development

### Running the Development Environment

1. Run `gulp`
2. Visit http://localhost:3000 in your browser

### Deploying on Google App Engine

```bash
gloud login
gulp deploy

# Alternatives
gulp deploy --project=vote4code
gulp deploy --project=vote4code --version=bar
gulp deploy --project=vote4code --version=bar --no-promote
```
