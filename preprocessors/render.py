import data_loader
import storage
from lxml import html, etree
from flask import render_template, render_template_string

def render_experience_template(template):
  """Loads the jobs.json file and renders a given template. Returns the formatted HTML."""
  data = data_loader.load_experience_file()
  template_html = ''
  for job in data:
    company = job['company']
    tenure = job['tenure']
    title = job['title']
    snippet = job['snippet']
    link = job['link']

    # Skills are hyphenated, and the description is an array of lines that should be joined by a
    # space. This is to make the JSON file more human readable.
    skills_delimited = ' - '.join(job['skills'])
    template_html += render_template(template,
                                     company=company,
                                     tenure=tenure,
                                     title=title,
                                     snippet=snippet,
                                     skills_delimited=skills_delimited,
                                     link=link)
  return template_html

def render_skills_template(template):
  """Loads the skills.json file and renders a given template. Returns the formatted HTML."""
  def _render_skill_template(skill_type):
    template_html = ''
    for idx, skill in enumerate(skill_type):
      skill_name = skill['name']
      percent = skill['percentage']
      index = 'item-' + str(idx)
      template_html += render_template(template,
                                       skill=skill_name,
                                       percent=percent,
                                       item_index=index)
    return template_html

  data = data_loader.load_skills_file()
  template_html = _render_skill_template(data['languages'])
  template_html += render_template(template, skill='', percent=0, item_index='')
  template_html += _render_skill_template(data['frameworks'])
  return template_html

def render_projects_grid_template(template, max_grid_items, show_more_button=False):
  """
    Renders the project grid template for a given number of projects.
    param template: the template to render.
    param max_grid_items: The number of items to show in the grid.
    param show_more_button: Whether the more button should be shown or not. Defaults to False.
  """
  data = data_loader.load_projects_file()
  template_html = ""

  for i in xrange(min(len(data), max_grid_items)):
    project = data[i]
    color = 'dark' if i % 2 == 0 else 'light'
    link = project['link']
    image = project['image_url']
    round_corners = 'rounded-corners' if project['round_corners'] else ''
    title = project['name']
    snippet = project['snippet']

    template_html += render_template(template,
                                     color=color,
                                     link=link,
                                     image=image,
                                     round_corners=round_corners,
                                     title=title,
                                     snippet=snippet)

  if show_more_button:
    with open('html/more_button.html') as f:
      template_html += f.read()

  return template_html


def render_experience_page(job):
  """Renders the experience page for a given job. Returns the templated HTML."""
  company = job['company']
  tenure = job['tenure']
  title = job['title']
  link = job['link']
  skills = job['skills']
  bannerurl = job['bannerurl']
  location = job['location']
  frameworks = job['frameworks']

  # Job description is a 2D array split into paragraphs. Join each line in a paragraph into a single
  # string.
  description = []
  for paragraph in job['description']:
    description.append(' '.join(paragraph))

  return render_template('experience_full_page_template.html',
                         company=company,
                         tenure=tenure,
                         title=title,
                         skills=skills,
                         frameworks=frameworks,
                         description=description,
                         bannerurl=bannerurl,
                         location=location)


def add_html_elements_inside_node(html_string, html_element, node_name, elements):
  """
    Inserts the new elements into a target node.
    param html_string: The string format of the HTML.
    param html_element: The element that will be the parent of the new elements.
    param node_name: The class name of the parent element.
    param elements: The string format of the HTML to be inserted.
  """

  # Get the target node from the HTML.
  root = html.fromstring(html_string)
  target_node = root.find('.//{}[@class="{}"]'.format(html_element, node_name))

  # Convert the new elements into an ETree and insert each one as a child of the target node.
  new_elements = html.fromstring(elements)
  for element in new_elements:
    target_node.append(element)
  return html.tostring(root)
