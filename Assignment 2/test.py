from nltk.tokenize import word_tokenize

filepath = './ex2-trace.tr'

packets = []

with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
      packets[i] = word_tokenize(line)
      i = i + 1

print(packets[1])
