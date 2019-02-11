#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

def logger(name):
	log = logging.getLogger(name)
	handler = logging.StreamHandler()
	handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s:%(module)s:%(threadName)s: %(message)s"))
	log.addHandler(handler)
	log.setLevel(logging.DEBUG)
	return log
