### this is a first script aiming at starting to explore the outline of project:
# getting the proper files from the UCSC REST-API
# parsing them, getting the proper sequence intervals

### 1: getting the proper JSON API. 
# gleaning through this page:
# http://genome-euro.ucsc.edu/goldenPath/help/api.html
# I came up with the following command to get what we need, and store it a json file.

##  :~$ wget -O- 'https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups' > pseudo_detector/genomicSuperDups.json
## but upon furthr thinking I figured that we should insert the downloading and verification of the database in the script

# Here I will now write some python code to begin to parse through it
# general idea on what I need to do here (among many other resources):

# https://realpython.com/lessons/what-is-json/             see video, min 1:40 (this is a whole mini-class on Json, which is pretty good)

# https://towardsdatascience.com/json-and-apis-with-python-fba329ef6ef0 is an even better resource

import json
import requests
import pandas as pd

dup_track= requests.get('https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups')
type(dup_track)
# <class 'requests.models.Response'>

myjson = dup_track.json()       # transform dup_track into a json file
type(myjson)
# myjson is a dictionary
# to see the structure in a helpful graphical rendition, insert https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups
# in the url section of a Firefox browser window. It's a dictionary with 9 items (downloadtime, downloadTimeStamp ...) 
# the critical one is genomicSuperDups, which is itself a dictionary with 640 keys (strings) and values (lists). The vast majority of these items have keys indicating
# patch names and have no value -empty list []; some, namely the chr1 thrugh 22, chrX anf chrY, have values consisting of a list of dictionaries (up to thousands per chromosome). 
# Each of these dictionaries represents a region of duplication: the key is just a progressive number, the value is a dictionary with keys that include
# chrom, chromStart, chromEnd, otherChrom, otherStart, otherEnd. Pandas can transform these lists of dictionaries into dataframes, where columns are 
# chromStart, chromEnd, otherChrom, otherStart, otherEnd etc... and rows are the 1 to n instances of duplicated regions.
# The advantage of having dataframes is vectorialisation (see below), which allow to go through it real fast 


roi= myjson['genomicSuperDups']['chr17']       # the chr will be given by the user from the argpare; see import_argparse.py (single position to begin with, we'll worry about bed files later)
print(type(roi))							   # I will work on this position for the time being as I work out the following steps. I will worry about input later
df= pd.DataFrame(roi)      # this make life much easier
print(df)

''' While optimisong the pandas part (vectorialisation etc.), focus on gene NF1, chr17 chromStart= 31212016, chromEnd= 31231713'''


# from this data frame, find if input is in the interval by vectorialisation, create an additional column of present-absent and by selcting columns and rows create a new data frame
# which will be saved as .csv and this will be the final output of the script.
# https://stackoverflow.com/questions/62646013/how-would-one-vectorize-over-a-pandas-dataframe-column-over-a-range-of-rows
# https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html       selecting rows and columns ~ tidyverse


# dup_track= requests.get('https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups').text

# the next block of code is in relation to how the input would be done if we were to pull from the API every time rather than have a copy of genomicSuperDups locally
# I will go for the local option, as the API has too many layers key:value to be practical
build= 'hg38'
chrom= 'chr7'
start= '150944961'
end= '150978321'



url = f'https://api.genome.ucsc.edu/getData/sequence?genome={build};chrom={chrom};start={start};end={end}'
url = f'https://api.genome.ucsc.edu/getData/sequence?genome={build};chrom={chrom};start={start};end={end}'



print(type(dup_track))


# not super-relevant now
def ucsc_api(url):
	'''Query UCSC api for ref and alt DNA seq'''
	r = requests.get(url) 
	myjson = r.json()
	return(myjson['dna']) # return(myjson['genomicSuperDups'])? maybe at this stage I could filter out the empty patches annotations

# type(dup_track)      # dup_track is now a string

# ### transform it into a Python Dictionary

# dup = json.loads(dup_track)

# type(dup)

# ### notice that one can get a python dictionary directly using the request module and the .json() suffix

# d_track = requests.get('https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups').json()

# type(d_track)

# ################ Parsing the dictionary

# print(dup.keys())
# type(dup['genomicSuperDups']) #genomicSuperDups is a dictionary

# print(dup['genomicSuperDups'].keys())
# keys= list(dup['genomicSuperDups'].keys())
# print(keys[0])
# print(type(keys[0]))
# len(keys)
# # genomicSupeDups is a dictionary whose 640 keys are strings representing chromosomal annotations



# print(dup['genomicSuperDups'].values())

# def listvalues(dictionary):
#     listnumber= 0
#     nonlistnumber= 0
#     for key, value in dictionary.items():
#         #print (type(value)) 
#         if type(value) != list:
#             print(key, ' value not a list')
#             nonlistnumber+= 1
#         elif (type(value)) == list:
#             print(key, ' IS A LIST')
#             listnumber+=1
#     print('there are ', listnumber, 'lists, and ', nonlistnumber, ' non-list values')

# listvalues(dup['genomicSuperDups'])












