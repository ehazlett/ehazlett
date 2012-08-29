#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"Evan Hazlett"
SITENAME = u"dev::ops"
SITEURL = 'http://evanhazlett.com'

TIMEZONE = 'America/Indiana/Indianapolis'

DEFAULT_LANG = 'en'
THEME = 'ehazlett'
# Blogroll
#LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
#          ('Python.org', 'http://python.org'),
#          ('Jinja2', 'http://jinja.pocoo.org'),)
LINKS = []
SOCIAL = []
# Social widget
#SOCIAL = (('twitter.com/ehazlett', '1'),)
# HACK to prevent git from complaining on build
FILES_TO_COPY = (('extra/placeholder', 'placeholder'),)

DEFAULT_PAGINATION = 10
