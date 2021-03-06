# vote4code

The vote4code website is place to upload two different versions of programming solutions to let the community vote for the best one. It's based on [**gae-init**](https://gae-init.appspot.com).

## Requirements

### Python
- [Python 2.7](https://www.python.org/downloads/)
- [pip](http://docs.gae-init.appspot.com/requirement/#pip)
- [virtualenv](http://docs.gae-init.appspot.com/requirement/#virtualenv)
- [Node.js](https://nodejs.org/en/)
- [Gulp](http://gulpjs.com/)
- [Yarn](https://yarnpkg.com/en/)

### Google Cloud Platform
- [Google Cloud SDK with App Engine](http://docs.gae-init.appspot.com/requirement/#gcloud)
- [Google App Engine SDK 1.9.53 for Python](https://cloud.google.com/appengine/docs/standard/python/download)

## Development

### First time

Execute `yarn` to install all the dependencies and then follow the next step

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

### Help

For more options execute:

```bash
gulp help
```
