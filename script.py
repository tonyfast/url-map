#!/usr/bin/env python

import re
import pprint
import sys
import json
from selenium import webdriver

global driver, dataset

driver  = webdriver.PhantomJS()
dataset = dict()

def get_page_anchors_for(url, recursive=False):
  # add a new array for the urls on this page
  if not url in dataset:
    dataset[url] = get_anchors_for_page(url)

    # Get the anchors of each new page
    if recursive:
      for url in dataset[url]:
        get_page_anchors_for(url)

def get_anchors_for_page(url):
  print "Processing anchors for: " + url
  driver.get(url)

  css = '[role="navigation"] * a[href], [role="main"] * a[href]'
  anchors = driver.find_elements_by_css_selector(css)
  urls = []

  for element in anchors:
    href = element.get_attribute('href')

    # skip if doesn't match *.mailchimp.com pattern
    pattern = re.compile("http(s?)://(.*\.)?mailchimp\.com(.*)")
    if not pattern.match(href):
      continue

    urls.append(href)

  return urls

get_page_anchors_for("http://mailchimp.com", recursive=True)

with open('./data.json', 'w') as outfile:
  json.dump(dataset, outfile)

driver.quit()