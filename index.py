#!/usr/bin/env python

print("Content-Type: text/html; charset=utf-8\n\r")
print("")

with open("index.html") as f:
	print(f.read())
