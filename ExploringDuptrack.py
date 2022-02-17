'''If a chromosomal position imputed by the user lies within a duplicated region in the genome,
   this script will return the genomic coordinates of the duplicated region(s)
'''


# 1. import required packages

import time
import os
import json
import requests
import argparse
import pandas as pd

start = time.time()

# 2. get in the proper working direcory

os.chdir("/home/giovanni/pseudo_detector")
# os.getcwd()

""" 3: parse arguments from command line
check out https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
"""

parser = argparse.ArgumentParser(
    description="A script intended to find whether a genomic position given by the user is found in a duplicated genomic region")
parser.add_argument("-c", "--chromosome", required=True, type=str,
                    help=
					"chromosome in which the genetic position lies [1 through 22, X, Y, M]")
parser.add_argument("-p", "--position", required=True,  type=int,
					help=
					"genomic position")


# parse the arguments

args = parser.parse_args()

"""4. Check whether the file containing the genomic coordinates of duplicated regions exists in the current directory.
If it does not, download it from the UCSC API. The file is quite large (40 Mb) and having a local copy of it
speeds up the execution of the script by about 9 sec.
"""


url= "https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups"

try:
	myjson= json.load(open("genomicSuperDups.json"))

except FileNotFoundError:
	print("File genomicSuperDups.json does not exist in the current directory; downloading from UCSC API.")
	dup_track= requests.get(url, allow_redirects=True).json()
	with open("genomicSuperDups.json", "w") as f:
		json.dump(dup_track, f)
	myjson= json.load(open("genomicSuperDups.json"))


"""to see the structure in a graphical rendition,
insert https://genome-euro.ucsc.edu/cgi-bin/hubApi/getData/track?genome=hg38;track=genomicSuperDups
in the url section of a Firefox browser window. It's a dictionary with 9 items (downloadtime, downloadTimeStamp, genomicSuperDups ...)
genomicSuperDups is itself a dictionary with 640 keys (strings) and values (lists). The items corresponding to """

# the chr will be given by the user from the argparse; see import_argparse.py
roi= myjson['genomicSuperDups']['chr'+ args.chromosome]


""" 5. transform the list of dictionaries into a data frame

chr1 through 22, chrX anf chrY, have values consisting of a list of dictionaries (up to thousands per chromosome).
Each of these dictionaries represents a region of duplication: the key is a progressive number, the value is a dictionary
with keys that include chrom, chromStart, chromEnd, otherChrom, otherStart, otherEnd.
Pandas can transform these lists of dictionaries into dataframes, where columns are chromStart, chromEnd, otherChrom, otherStart, otherEnd etc...
and rows are the 1 to n instances of duplicated regions.
The advantage of dataframes is vectorization (see below)
"""

df= pd.DataFrame(roi)
"""list of dictionaries is transformed in pandas dataframe

6. check whether the position provided by the user is within an annotated duplicated region

Within this data frame, find if input position is included within an interval representing a duplicated region.

For testing purpose, input positions within chr17 chromStart= 31212016, chromEnd= 31231713
or chr17 position= 83236265
"""

position= args.position

# create a new column displaying a 'Yes' string for those duplicated regions that contain the genomic position provided by the user
df.loc[(df['chromStart']<= position) & (df['chromEnd']>= position), 'Included in Dup interval']= 'Yes'


# 7. create and print a new dataframe containing the rows that have a Yes value in the last column


df1= (df.loc[df['Included in Dup interval']=='Yes'])[['chrom', 'chromStart', 'chromEnd', 'name', 'strand', 'otherChrom', 'otherStart', 'otherEnd', 'fracMatch']]

if not df1.empty:
	print(df1)
else:
	print("The provided genomic position ", "chr"+ args.chromosome, position,  " does not lie within a duplicated region.")

# 8. save dataframe as a csv file
df1.to_csv('genomic_duplicates.csv', index=False)

end = time.time()
print("time elapsed: ", round(end - start, 4))
















