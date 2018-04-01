import os

_BUCKET_NAME = 'jackarendt-website'
_BUCKET_HOST = 'https://storage.googleapis.com/'
_BUCKET_TEMPLATE = "{{bucket_url}}"

def replace_bucket_name(html):
  return html.replace(_BUCKET_TEMPLATE, _BUCKET_HOST + _BUCKET_NAME)
