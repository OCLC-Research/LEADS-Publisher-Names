#!/usr/bin/python 


# Interpret the value of the 008/24-27 (nature of contentsd) as a base-29
# integer and convert to a base-10 integer to encode the various letters of the
# value down to a single value


#     # - No specified nature of contents
#     a - Abstracts/summaries
#     b - Bibliographies
#     c - Catalogs
#     d - Dictionaries
#     e - Encyclopedias
#     f - Handbooks
#     g - Legal articles
#     i - Indexes
#     j - Patent document
#     k - Discographies
#     l - Legislation
#     m - Theses
#     n - Surveys of literature in a subject area
#     o - Reviews
#     p - Programmed texts
#     q - Filmographies
#     r - Directories
#     s - Statistics
#     t - Technical reports
#     u - Standards/specifications
#     v - Legal cases and case notes
#     w - Law reports and digests
#     y - Yearbooks
#     z - Treaties
#     2 - Offprints
#     5 - Calendars
#     6 - Comics/graphic novels
#     | - No attempt to code


# Sample values from the 1k set
sample = [
    '    ',
    '  d ',
    '6   ', 
    'b   ', 
    'bc  ', 
    'bd  ', 
    'be  ', 
    'bf  ', 
    'bfkq', 
    'bg  ', 
    'bm  ', 
    'bs  ', 
    'bt  ', 
    'bu  ', 
    'c   ', 
    'd   ', 
    'e   ', 
    'efr ', 
    'f   ', 
    'im  ', 
    'ir  ', 
    'k   ', 
    'm   ', 
    'mb  ', 
    'p   ', 
    'r   ', 
    's   ', 
    't   ', 
    'u   '
]

# per https://www.loc.gov/marc/bibliographic/bd008b.html
# alpha is the list of valid values in the 008/24-27
alpha = [ ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z', '2', '5', '6', '|' ]

# base is the number of letters in the alphabet
base=len(alpha)

def encode(s):
    val=0  # initialize the value of the encoded number
    exp=len(s)-1 # calculate the exponent for the first digit (taking the characters as big endian)
    for x in sorted(s): # for each character in the 008/24-27, after sorting them
        n=alpha.index(x) # get the index of the character in the alphabet, eg ' ' = 0, d = ' 4'
        val = val + (n * (base ** exp)) # add the base-29 value of this digit to the running total
        exp = exp - 1 # decrease the exponent by one for the next iteration
    return(val) # return the calculated integer as a decimal

for s in sample:
    print("'" + s + "' - '" + ''.join(sorted(s)) + "' = " + str(encode(s)))

