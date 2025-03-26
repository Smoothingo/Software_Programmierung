import sys
import re

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        word = word.lower()
        word = re.sub('[^a-zA-Z]+', '', word)
        if word != '':
            print(f"{word}\t1")