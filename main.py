import logging
import os
from flask import Flask, render_template, request
from preprocessors import storage

app = Flask(__name__)

@app.route('/')
def root():
  """Entry point to website. Return home.html and populate it with latest data."""
  with open('html/home.html') as f:
    html = f.read()
    return storage.replace_bucket_name(html)

@app.errorhandler(500)
def server_error(e):
  """Log the exception, and send back a custom error page."""
  logging.exception('An error occurred during a request.')
  return """
  An internal error occurred: <pre>{}</pre>
  See logs for full stacktrace.
  """.format(e), 500
