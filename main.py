import logging
import os
from flask import Flask, request, redirect
from preprocessors import *

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

@app.errorhandler(500)
def server_error(e):
  """Log the exception, and send back a custom error page."""
  logging.exception('An error occurred during a request.')
  return """
  An internal error occurred: <pre>{}</pre>
  See logs for full stacktrace.
  """.format(e), 500
