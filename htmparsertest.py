htmlSource = """
<html>
<head>
<title>Test page</title>
</head>
<body>
<ul>
<li><a href=index.html>Home</a></li>
<li><a href=toc.html>Table of contents</a></li>
<li><a href=history.html>Revision history</a></li>
Dive Into Python
108
</body>
</html>

"""
from sgmllib import SGMLParser

from BaseHTMLProcessor import BaseHTMLProcessor
parser = BaseHTMLProcessor()
parser.feed(htmlSource)
print parser.output()