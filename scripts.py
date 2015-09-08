# Just copy + paste from the PDF and deal with the crappy formatting
print "\n".join([i for a in x.split("\n") for i in a.split('.') if len(i) > 0])
