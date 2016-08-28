d = {"surname":"Lucas",
    "firstname":"Richard",
    "dob":"14-Aug-1964"
    }

print '"\n".join(d.keys())'
print "\n".join(d.keys())
print ""

print '"\n".join(d.values())'
print "\n".join(d.values())
print ""

print '"\n".join("%s:%s" % (k,v) for k,v in d.items())'
print "\n".join("%s:%s" % (k,v) for k,v in d.items())

lengths = [ len(elm) for elm in d.values()]
print "\n".join("%d" % (v) for v in lengths)