#!/usr/bin/python

import re

# Like what I said in the conference, I am having the following problem. I want
# to have the abilities to split strings like the following: "A is a part of
# B", "A, a part of B", "A, A Part of B" and "A, a Part of B". In R, all these
# examples can be split by "( is|,) (a|A) (Part|part) of". However, I do not
# think this works at all in Python. (I know in general that regex in Python
# and R is different. But I never imagined it is this different.) It would be
# super great if you could point me to some basic strategies of doing this.


strings = [
    "A is a part of B",
    "A, a part of B",
    "A, A Part of B",
    "A, a Part of B"
    ]

exp = r"( is|,) a part of ?"
for s in strings:
    split = re.split(exp, s, flags=re.IGNORECASE)
    print("'" + split[0] + "' - '" + split[-1] + "'")

    

