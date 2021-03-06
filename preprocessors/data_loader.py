import json

def load_experience_file():
  """Loads the jobs.json file and converts it to JSON."""
  return json.load(open('data/jobs.json'))

def load_skills_file():
  """Loads the skills.json file and converts it to JSON."""
  return json.load(open('data/skills.json'))

def load_projects_file():
  """Loads the projects.json file and converts it to JSON."""
  return json.load(open('data/projects.json'))

def target_experience(job_url_parameter):
  """Returns the job that matches the supplied URL parameter."""
  if job_url_parameter is None:
    return None

  return _target_item(load_experience_file(), job_url_parameter)

def target_project(project_url_parameter):
  if project_url_parameter is None:
    return None

  return _target_item(load_projects_file(), project_url_parameter)


def _target_item(data, target_url_parameter):
    for item in data:
      if item["urlname"].lower() == target_url_parameter.lower():
        return item
    return None
