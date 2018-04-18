# Personal Website
## Overview
- Server side rendered using templates and inserting DOM nodes using lxml.
- Hosted on GCP.
- Server written in Python using Flask. I wanted to use express + node, but wanted a new challenge.
- Data is hosted on GCP for quick rendering of pages.
- Assets are hosted on Google Cloud Storage.
- Uses https by default.

## Directory Structure
- Data
- - JSON data to populate dynamic web pages.
- design
- - ai
- - - Adobe Illustrator files
- - png
- - - PNG files
- - svg
- - - SVG files
- html
- - Static HTML files that don't need to be templatized.
- preprocessors
- - Python lib that renders the html and prepares to be viewed.
- stylesheets
- - CSS files
- templates
- - HTML template files.
