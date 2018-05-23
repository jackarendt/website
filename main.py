import json
import logging
import os
import re
import httplib2
from flask import Flask, request, redirect
from mailgun import *
from preprocessors import *
from urllib import urlencode

app = Flask(__name__)

@app.route('/')
def root():
  """Entry point to website. Return home.html and populate it with latest data."""
  with open('html/home.html') as f:
    html = f.read()

    # Render experience template.
    expierience = render.render_experience_template('experience_template.html')
    html = render.add_html_elements_inside_node(html, 'ul', 'experiences', expierience)

    # Render skills template.
    skills = render.render_skills_template('skills_list_item.html')
    html = render.add_html_elements_inside_node(html, 'dl', 'skills', skills)

    projects = render.render_projects_grid_template('projects_template.html', 5, True)
    html = render.add_html_elements_inside_node(html, 'div', 'projects-container', projects)

    # Return formatted HTML.
    return storage.replace_bucket_name(html)

@app.route('/experience')
def experience():
  """Loads the job experience template. Redirects to experiences div if no valid job is found."""
  job = data_loader.target_experience(request.args.get('job'))
  if job is None:
    # Redirect to the home page focused at the experience div.
    return redirect('/#experience', 302)

  # Render the template and replace all instances of the bucket name.
  html = render.render_experience_page(job)
  html = storage.replace_bucket_name(html)
  return html

@app.route('/projects')
def projects():
  """Loads the projects page either for a specific page, or all projects."""
  project = data_loader.target_project(request.args.get('project'))
  if project is None:
    with open('html/projects.html') as f:
      html = f.read()
      projects = render.render_projects_grid_template('projects_template.html')
      html = render.add_html_elements_inside_node(html, 'div', 'projects-container', projects)
      html = storage.replace_bucket_name(html)
    return html

  # Load the project page for a specific project.
  html = render.render_projects_page(project)
  html = storage.replace_bucket_name(html)
  return html

@app.route('/contact')
def contact():
  """Sends the form to mailgun and returns either a success or error message."""
  name = request.args.get('name')
  email = request.args.get('email')
  subject = request.args.get('subject')
  message = request.args.get('message')

  # Verify all fields are filled out.
  if not name or not subject or not message or not email:
    retval = {'success' : False, 'message' : 'Please fill out all fields.'}
    return json.dumps(retval)

  # Verify the email address is valid.
  if not re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
    retval = {'success' : False, 'message' : 'Please provide a valid email address.'}
    return json.dumps(retval)

  http = httplib2.Http()
  http.add_credentials('api', '{}'.format(MAILGUN_API_KEY))

  url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
  data = {
    'from': '{} <mailgun@{}>'.format(name, MAILGUN_DOMAIN_NAME),
    'to': 'jack@jackarendt.com',
    'subject': '{}'.format(subject),
    'text': 'Return Email: {}\n\n{}'.format(email, message)
  }

  # Post the mail form.
  resp, content = http.request(url, 'POST', urlencode(data),
                               headers={'Content-Type': 'application/x-www-form-urlencoded'})

  # Return an error if something goes wrong.
  if resp.status != 200:
    retval = {'success' : False, 'message' : 'Something went wrong. Try again later.'}
    return json.dumps(retval)

  # Return that the message was successfully sent.
  retval = {'success' : True, 'message' : 'Thank you, I\'ll be in touch shortly.'}
  return json.dumps(retval)

@app.errorhandler(500)
def server_error(e):
  """Log the exception, and send back a custom error page."""
  logging.exception('An error occurred during a request.')
  html = render.render_template('error_message_template.html',
                                title='Hmm, something went wrong.',
                                subtitle='An internal error occurred, that\'s all I know.')
  html = storage.replace_bucket_name(html)
  return html

@app.errorhandler(404)
def unknown_page(e):
  """Send the user to a specific 404 page."""
  html = render.render_template('error_message_template.html',
                                title='That\'s a 404.',
                                subtitle='Looks like you made a wrong turn.')
  html = storage.replace_bucket_name(html)
  return html
