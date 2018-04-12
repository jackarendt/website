import json
from lxml import html, etree
from flask import render_template, render_template_string

def render_experience_template(template, hyphenate_skills):
  """Loads the jobs.json file and renders a given template. Returns the formatted HTML."""
  data = json.load(open('data/jobs.json'))
  template_html = ""
  for job in data:
    company = job["company"]
    tenure = job["tenure"]
    title = job["title"]
    snippet = job["snippet"]
    link = job["link"]

    # Skills are hyphenated, and the description is an array of lines that should be joined by a
    # space. This is to make the JSON file more human readable.
    skills_delimited = " - ".join(job["skills"])
    description = " ".join(job["description"])
    template_html += render_template(template,
                                     company=company,
                                     tenure=tenure,
                                     title=title,
                                     snippet=snippet,
                                     skills_delimited=skills_delimited,
                                     description=description,
                                     link=link)
  return template_html

def render_skills_template(template):
  """Loads the skills.json file and renders a given template. Returns the formatted HTML."""
  def _render_skill_template(skill_type):
    template_html = ""
    for idx, skill in enumerate(skill_type):
      skill_name = skill["name"]
      percent = skill["percentage"]
      index = "item-" + str(idx)
      template_html += render_template(template,
                                       skill=skill_name,
                                       percent=percent,
                                       item_index=index)
    return template_html

  data = json.load(open('data/skills.json'))
  template_html = _render_skill_template(data["languages"])
  template_html += render_template(template, skill="", percent=0, item_index="")
  template_html += _render_skill_template(data["frameworks"])
  return template_html


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
  target_node = root.find(".//{}[@class='{}']".format(html_element, node_name))

  # Convert the new elements into an ETree and insert each one as a child of the target node.
  new_elements = html.fromstring(elements)
  for element in new_elements:
    target_node.append(element)
  return html.tostring(root)
