# pseudo_detector

#What does this programme do?
Pseudo_detector is a programme that accesses the 'Segmental Dups'from UCSC REST-API and generates a JSON dictionary,
this dictionary is transformed into a dataframe which is used to find duplicated regions within given genomic coordinates.

#What are the typical cases for this programme?
THis programme is used to identify duplicated genomic regions, its application can be used within both and research and
clinical environment following  testing and validation. It is aimed to help clinical scientists  flag for variants in duplicated
regions when running identifying pathogenic variants.

#What data is required for this programme to run?
The programme requires a genomic region to query.

#What does the programme output?
This programme outputs a new dataframe containing the rows that have a Yes value in the last column,
and a chrom, chromStart, chromEnd, strand, otherChrom, otherStart, otherEnd, 'fracMatch'.
Ultimately, the dataframe includes the coordinates of the region in a given position and the genomic
coordinates of the duplicated region/s.