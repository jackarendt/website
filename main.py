import logging
import os
from flask import Flask, request
from preprocessors import storage, render

app = Flask(__name__)

@app.route('/')
def root():
  """Entry point to website. Return home.html and populate it with latest data."""
  with open('html/home.html') as f:
    html = f.read()
    html = storage.replace_bucket_name(html)

    # Render experience template.
    expierience = render.render_experience_template('experience_template.html', True)
    html = render.add_html_elements_inside_node(html, 'ul', 'experiences', expierience)

    # Render skills template.
    skills = render.render_skills_template('skills_list_item.html')
    html = render.add_html_elements_inside_node(html, 'dl', 'skills', skills)

    # Return formatted HTML.
    return html

@app.errorhandler(500)
def server_error(e):
  """Log the exception, and send back a custom error page."""
  logging.exception('An error occurred during a request.')
  return """
  An internal error occurred: <pre>{}</pre>
  See logs for full stacktrace.
  """.format(e), 500
