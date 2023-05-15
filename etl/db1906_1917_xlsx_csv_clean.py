import pandas as pd
import numpy as np 
from fold_to_ascii import fold # for handling diacritics and other special char stuff
import unidecode

# read in excel file
df = pd.read_excel("../data/source/NAH inv  941 dienstboderegister 1906-1917.xlsx", dtype='str', na_values='---')

# add more informative and 'clean' column names
df.columns = ['regel', 'datumInschrijving', 'familienaam', 'voornaam', 'geboorteDatum', 'geboortePlaats',
       'burgerlijkeStaat', 'religie', 'beroep', 'verblijf', 'aankomstDatum',
       'vorigeWoonplaats', 'vertrekDatum', 'vertrekPlaats', 'opmerkingen', 'blad']

################################ date of arrival ##############################

df['aankomstDatumCl'] = df['aankomstDatum'].astype(str)
#### show all dates that do not match 2digits-2digits-4digits
# x = df['aankomstDatum'][~df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
# print(x.dropna())

#44          16-12-?
#106     17 -01-1914
#220       13-041912
#353     11-12-11917
#375     19-02-11908
#379         
#588
#705      15-09-1918
#711     07-03-1919
#779
#799     16-01--1913
#898      22-04-????
#955         18-05-?
#1039     01-05-1909
#1040         01-05-

# pickup trailing spaces
df['aankomstDatumCl'] = df['aankomstDatumCl'].str.strip()

df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('16-12-?', '16-12-xxxx')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('17 -01-1914', '17-01-1914')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('13-041912', '13-04-1912')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('11-12-11917', '11-12-1917')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('19-02-11908', '19-02-1908')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('15-09-1918', '15-09-1918')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('07-03-1919 ', '07-03-1919')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('16-01--1913', '16-01-1913')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('22-04-????', '22-04-xxxx')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('01-05-1909', '01-05-1909')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('01-05-', '01-05-xxxx')

# y = df['aankomstDatum'][~df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
# print(y.dropna())
#44         16-12-?
#379        21-11-?
#588
#779
#898     22-04-????
#955        18-05-?
#1040        01-05-

# ok let's kill the remaing values
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('25-14-1917', '25-xx-1917') # appeared to be wrong as well

#### so now only preserve values of the pattern 2digits-2digits-4digits
df['aankomstDatumCl'] = df['aankomstDatumCl'][df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]

# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD
df['aankomstDatumCl'] = pd.to_datetime(df['aankomstDatumCl'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
# print(df['aankomstDatumCl'].dropna())

################################ date of registration ##############################

df['datumInschrijvingCl'] = df['datumInschrijving'].astype(str)
#### show all dates that do not match 2digits-2digits-4digits
# x = df['datumInschrijving'][~df['datumInschrijvingCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
# print(x.dropna())

#   16          27-03- ?
#   25               Leeg
#   27               Leeg
#   52         14 09-1908
#   70        `07-01-1910
#   87         11-12-?
#  117        17 07-1915
#  142
#  182              Leeg
#  192              Leeg
#  264        ? -01-1900
#  313
#  360     Niets vermeld
#  362     Niets vermeld
#  379           24-11-?
#  466              Leeg
#  517      26-10- -----
#  610              Leeg
#  632        10-01-1912
#  656              Leeg
#  717              Leeg
#  719           05-1900
#  835              Leeg
#  874        10-05-1-18
#  881              Leeg
#  971        05-04-1918
#  991              Leeg
#  993       14-07- 1908
# 1021             Leeg
# 1023              U.
# 1062           14-11-
# 1100             Leeg
# 1167             Leeg
# 1169               IJ
# 1172       Janu. 1900
# 1192             Leeg
# 1199             Leeg
# 1201        02-091918

df['datumInschrijvingCl'] = df['datumInschrijvingCl'].str.strip()
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('14 09-1908',  '14-09-1908')
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace("`07-01-1910", '07-01-1910')
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('17 07-1915',  '17-07-1915')
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('10-01-1912',  '10-01-1912')
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('10-05-1-18',  '10-05-1918')
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('14-07- 1908', '14-07-1908')
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('02-091918',   '02-09-1918')

#y = df['datumInschrijving'][~df['datumInschrijvingCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
#print(y.dropna())

# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['datumInschrijvingCl'] = df['datumInschrijvingCl'][df['datumInschrijvingCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
#print(df['datumInschrijvingCl'].dropna())

################################ date of departure ##############################

df['vertrekDatumCl'] = df['vertrekDatum'].astype(str)

# pickup trailing spaces
df['vertrekDatumCl'] = df['vertrekDatumCl'].str.strip()


#### show all dates that do not match 2digits-2digits-4digits
#x = df['vertrekDatum'][~df['vertrekDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
#print(x.dropna())
# 32                    04-06-1717
# 44                      28-12- ?
# 129     ( 04-12-1916) 10-02-1920 # check with original source
# 206                  ? - 12-1909
# 346                    31-101918
# 477                       20-10-
# 665                  07-02-19141
# 673                    29-07- ……
# 852                      05-11-?
# 998                    29-071913
# 1040                      03-10-
# 1129     31-08-1910,  28-04-1914 # check with orignal source
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('04-06-1717', '04-06-1917')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('31-101918', '31-10-1918')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('07-02-19141', '07-02-1914')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('29-071913', '29-07-1913')

#y = df['vertrekDatum'][~df['vertrekDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
#print(y.dropna())

# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['vertrekDatumCl'] = df['vertrekDatumCl'][df['vertrekDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
# print(df['vertrekDatumCl'].dropna())

# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD
df['vertrekDatumCl'] = pd.to_datetime(df['vertrekDatumCl'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')
# print(df['vertrekDatumCl'].dropna())

# now go through burgerLinker data cleaning steps
# https://github.com/CLARIAH/burgerLinker/wiki/01.-Data-standardization

##############################################
#                                            #
# burgerLinker cleaning dates and formatting #
#                                            #
##############################################


# 1 date variables (put into YYYY-MM-DD format)
df['geboorteDatumCl'] = df['geboorteDatum'].astype(str)

#### show all dates that do not match 2digits-2digits-4digits
# x = df['geboorteDatum'][~df['geboorteDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
# print(x.dropna())
# 16       28-08- ?
# 95       21-111892
# 249      23-101894
# 267    01-07--1889
# 281      13-101894
# 379        06-05-?
# 418    "22-02-1887
# 673        06-02-
# 852        26-02-?
# 898     05-09-????

# pickup trailing spaces
df['geboorteDatumCl'] = df['geboorteDatumCl'].str.strip()

df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('21-111892', '21-11-1892')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('23-101894', '23-10-1894')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('01-07--1889', '01-07-1889')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('13-101894', '13-10-1894')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('"22-02-1887', '22-02-1887')

#y = df['geboorteDatum'][~df['geboorteDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
#print(y.dropna())
# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['geboorteDatumCl'] = df['geboorteDatumCl'][df['geboorteDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]

# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD 
df['geboorteDatumCl'] = pd.to_datetime(df['geboorteDatumCl'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
print(df['geboorteDatumCl'].dropna())

#############################################
#                                           #
# burgerLinker familynames without prefixes #
#                                           #
#############################################

df['familienaamCl'] = df['familienaam'].astype(str)

# These 'regel' ids have no valid entry for last entry: 243,503,1025,1171
# print(df['familienaamCl'][df['regel']=='243'])
# print(df['familienaamCl'][df['regel']=='503'])
# print(df['familienaamCl'][df['regel']=='1025'])
# print(df['familienaamCl'][df['regel']=='1171'])
# 241    Leeg
# Name: familienaamCl, dtype: object
# 501    Vervolg  Blad 161
# Name: familienaamCl, dtype: object
# 1023    Verder leeg
# Name: familienaamCl, dtype: object
# 1169    Verder leeg
# Name: familienaamCl, dtype: object

df['familienaamCl'][df['regel']=='243']= np.NaN
df['familienaamCl'][df['regel']=='503']= np.NaN
df['familienaamCl'][df['regel']=='1025']= np.NaN
df['familienaamCl'][df['regel']=='1171']= np.NaN

# print(df['familienaamCl'][df['regel']=='243'])
# print(df['familienaamCl'][df['regel']=='503'])
# print(df['familienaamCl'][df['regel']=='1025'])
# print(df['familienaamCl'][df['regel']=='1171'])


df['familienaamCl'] = df['familienaamCl'].str.split(' ').str[0]
# print(df['familienaamCl'].dropna())

#####################################################
#                                                   #
# burgerLinker replace specific characters in names #
#                                                   #
# 'ch' to 'g'                                       #
# 'c'  to 'k'                                       #
# 'z'  to 's'                                       #
# 'ph' to 'f'                                       #
# 'ij' to 'y'                                       #
#####################################################

# df['familienaamCl'] = (df['familienaamCl'].str.lower().str.strip().map(lambda x: unidecode.unidecode(x)) )
df['familienaamCl'] = (df['familienaamCl'].str.lower().str.strip() )


#df['familienaamCl'] = unidecode.unidecode(df['familienaamCl'])
# pd.set_option('display.max_rows', None)

print(df['familienaamCl'])

# From output below: FutureWarning: The default value of regex will change from True to False in a future version.
df['familienaamCl'] = df['familienaamCl'].str.replace(r' ', '')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'\.', '')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(?i)ch', 'g') #(?i) ignores case
df['familienaamCl'] = df['familienaamCl'].str.replace(r'([Cc])', 'k') # either capital C or regular c
df['familienaamCl'] = df['familienaamCl'].str.replace(r'([Zz])', 's')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(?i)ph', 'f')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(?i)ij', 'y')

print(df['familienaamCl'].dropna())

df['familienaamCl'] = df['familienaamCl'].replace('nan', '') # should be fixed in pandas 2.4

df['voornaamCl'] = df['voornaam'].astype(str) # bug in pandas NaN is converted to nan
#df['voornaamCl'] = (df['voornaamCl'].str.lower()
#                                    .str.strip() 
#                                    .map(lambda x: unidecode.unidecode(x)) )
df['voornaamCl'] = df['voornaamCl'].str.replace(r' ', '')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'\.', '')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'(?i)ch', 'g')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'([Cc])', 'k')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'([Zz])', 's')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'(?i)ph', 'f')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'(?i)ij', 'y')
df['voornaamCl'] = df['voornaamCl'].str.replace(r'(?i)nietsvermeld', '')
df['voornaamCl'] = df['voornaamCl'].replace('nan', '') # should be fixed in pandas 2.4

# create id for record
df['registrationId'] = 'NAH940-DBRegister-1906-1917-' + df['regel'].astype(str)

# check whether persons appear more than once
# this is the case when lastname + firstname + birthdate match
dfBak = df
#df[['familienaamCl','voornaamCl','geboorteDatumCl']].value_counts()



df['personId'] = df['regel']

# dropping any rows with NaN or "" empty strings
df = df.dropna(axis=0, subset=['geboorteDatumCl'])
df = df[df.familienaamCl != '']
df = df[df.voornaamCl != '']

# dropping dubplicates based on given name, family name and birth date
df = df.drop_duplicates(subset=['familienaamCl','voornaamCl','geboorteDatumCl'], keep = 'first')

      
# write out orignal data as .csv file
dfBak.to_csv("../data/derived/db1906_1917_clean_unique.csv", index = False)

       


