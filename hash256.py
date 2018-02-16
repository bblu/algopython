import hashlib

ctx = "A own B 50RMB"
print "sha256(%s)" % ctx, hashlib.sha256(ctx).hexdigest()
