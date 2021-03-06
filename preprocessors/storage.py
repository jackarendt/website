_BUCKET_NAME = 'jackarendt-website'
_BUCKET_HOST = 'https://storage.googleapis.com/'
_BUCKET_TEMPLATE = "[[bucket_url]]"

def replace_bucket_name(html):
  """Replaces all instances of the bucket tag with the full path."""
  expanded = html.replace(_BUCKET_TEMPLATE, full_storage_path())

  # Replace the URL escaped string as well.
  return expanded.replace('%5B%5Bbucket_url%5D%5D', full_storage_path())

def full_storage_path():
  """Returns the full path of the storage bucket."""
  return _BUCKET_HOST + _BUCKET_NAME
