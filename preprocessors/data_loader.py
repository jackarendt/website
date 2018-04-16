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
  if job is None:
    return None

  jobs = load_experience_file()
  for exp in jobs:
    if exp["urlname"].lower() == job_url_parameter.lower():
      return exp
  return None
