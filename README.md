===============================
SHA256 Personnal Implementation
===============================

This is my own implementation for Secure Hash Algorithm. It's just for a personnal interest and curiosity. Complexity and execution time are not so good.
Typical usage looks like this:

	#!/usr/bin/python
	#-*- coding: utf-8 -*-

	from sha256 import SHA256

  s = SHA256('Hello World')

  print(s.encode())


INSTALLATION
============

* clone and "pip install . "
