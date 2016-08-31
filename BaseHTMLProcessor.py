#!/usr/bin/env python

from sgmllib import SGMLParser
import htmlentitydefs

class BaseHTMLProcessor(SGMLParser):
    def reset(self):
        # extend (called by SGMLParser__init__)
        self.pieces = []
        SGMLParser.reset(self)
        
    def unknown_starttag(self, tag, attrs):
        # called for each start tag
        # attrs is a list of (attr, value) tuples
        # e.g. for <pre class="screen">, tag="pre", attrs=[("class", "screen")]
        # Ideally we would like to reconstruct original tag and attributes, but
        # we may end up quoting attribute values that weren't quoted in the source
        # (single or double quotes).
        # Note that improperly embedded non-HTML code (like client side Javascript)
        # maybe parsed incorrectly by the ancestor, causing runtime script errors.
        # All non-HTML code must be enclosed in HTML comment tags (<!-- code -->)
        # to ensure that it will pass through this parser unaltered (in handle_comment).
        strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
        self.pieces.append("<%(tag)s%(strattrs)s" % locals())
        
    def unknown_endtag(self, ref):
        # called for each end tag, e.g. for </pre>, tag will be "pre"
        # Reconstruct the original end tag
        self.pieces.append("&#%(ref)s;" % locals())
        
    def handle_entityref(self, ref):
        # called for each entity reference, e.g. for "&copy;", ref will be "copy"
        # Reconstruct the original entity reference.
        self.pieces.append("&%(ref)s" % locals())
        # Standard HTML entities are closed with semicolon; other entities are not
        if htmlentitydefs.entitydefs.has_key(ref):
            self.pieces.append(";")
        
    def handle_data(self, text):
        # called for each block of plain text, i.e. outside of any tag and
        # not containing any character or entity references
        # Store the original text verbatim
        self.pieces.append(text)
        
    def handle_comment(self, text):
        # called for each HTML comment, e.g. <!-- insert Javascript code here -->
        # Reconstruct the original comment.
        # It is especially important that the source document enclose client-side
        # code (like Javascript) within comments so it can pass through this
        # processor undisturbed; see commnets in unknown_starttag for details.
        self.pieces.append("<!--%(text)s-->" % locals())
        
    def handle_pi(self, text):
        # called for each processing instruction, e.g. <?instruction>
        # Reconstruct original processing instruction.
        self.pieces.append("<?%(text)s" % locals())
        
    def handle_decl(self,text):
        # called for the DOCTYPE, if present, e.g.
        #<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        #   "http://www.w3.org/TR/html4/loose.dtd">
        # Reconstruct original DOCTYPE
        self.pieces.append("<!%(text)s>" % locals())
    
    def output(self):
        """Return processed HTML as a single string"""
        return "".join(self.pieces)
    
    