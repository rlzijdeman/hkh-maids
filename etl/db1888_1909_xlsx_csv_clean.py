import pandas as pd
import numpy as np 
from fold_to_ascii import fold # for handling diacritics and other special char stuff
import unidecode

# read in excel file
df = pd.read_excel("../data/source/NAH inv 940 dienstboderegister 1888-1909.xlsx", dtype='str', na_values='---')

# add more informative and 'clean' column names
df.columns = ['regel', 'datumInschrijving', 'familienaam', 'voornaam', 'geboorteDatum', 'geboortePlaats',
       'burgerlijkeStaat', 'religie', 'beroep', 'verblijf', 'aankomstDatum',
       'vorigeWoonplaats', 'vertrekDatum', 'vertrekPlaats', 'opmerkingen', 'blad']


################################ date of arrival ##############################

df['aankomstDatumCl'] = df['aankomstDatum'].astype(str)
#### show all dates that do not match 2digits-2digits-4digits
x = df['aankomstDatum'][~df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
# print(x.dropna())

# output of wrong values
# 72           30-05-1885
# 335     19-02-1894 Eelde
# 373           15-02-????
# 698          05-08-1904
# 865          05-05-18893
# 935            2-09-1902
# 946          06-101-1903
# 951            20-7-1904
# 1406       deel K bl.165
# 1407          deel A 207
# 532         24--04-1902
# 1634                   -
# 1662         26-07--1895
# 1853          05-05-190?

# pickup trailing spaces
df['aankomstDatumCl'] = df['aankomstDatumCl'].str.strip()

df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('19-02-1894 Eelde', '19-02-1894')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('2-09-1902', '02-09-1902')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('06-101-1903', '06-11-1903') # 06-101-1903 can't be 06-11 because entry is in October
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('20-7-1904', '20-07-1904')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('24--04-1902', '24-04-1902')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('26-07--1895', '26-07-1895')
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('05-05-190?', '05-05-1900') # based on regisration year

y = df['aankomstDatum'][~df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(y.dropna())
# 373        15-02-????
# 865       05-05-18893
# 1406    deel K bl.165
# 1407       deel A 207
# 1634                -

# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['aankomstDatumCl'] = df['aankomstDatumCl'][df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]


# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD
df['aankomstDatumCl'] = pd.to_datetime(df['aankomstDatumCl'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

print(df['aankomstDatumCl'])
################################ date of registration ##############################

df['datumInschrijvingCl'] = df['datumInschrijving'].astype(str)
#### show all dates that do not match 2digits-2digits-4digits
x = df['datumInschrijving'][~df['datumInschrijvingCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(x.dropna())
# 57      02-12-????
# 139
# 362     19-06-????
# 455       11-11-??
# 540     02-06-????
# 655             de
# 973     onleesbaar
# 1195    15-08-19??
# 1368      25-02-??


# pickup trailing spaces
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].str.strip()
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('02-12-????', '02-12-1904') #based on aankomstdatum: 01-12-1904
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('11-11-??', '11-11-1904') #based on aankomstdatum: 09-11-1904
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('15-08-19??', '15-08-1904') #based on aankomstdatum: 21-07-1904

y = df['datumInschrijving'][~df['datumInschrijvingCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(y.dropna())
# 139
# 362     19-06-????
# 540     02-06-????
# 655             de
# 973     onleesbaar
# 1368      25-02-??

# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['datumInschrijvingCl'] = df['datumInschrijvingCl'][df['datumInschrijvingCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]

# also kill other non xsd-date compliant values... 
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-00-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-01-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-02-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-04-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-05-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-06-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-09-1900', np.NaN)
df['datumInschrijvingCl'] = df['datumInschrijvingCl'].replace('00-01-1899', np.NaN)


# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD
df['datumInschrijvingCl'] = pd.to_datetime(df['datumInschrijvingCl'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')


################################ date of departure ##############################

df['vertrekDatumCl'] = df['vertrekDatum'].astype(str)

# pickup trailing spaces
df['vertrekDatumCl'] = df['vertrekDatumCl'].str.strip()


#### show all dates that do not match 2digits-2digits-4digits
x = df['vertrekDatum'][~df['vertrekDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(x.dropna())

# 254        31-01-??
# 527      09-03-19??
# 610       07-081891
# 1077    110-04-1889
# 1324    2/6-07-1906
# 1487              -
# 1535      0608-1906
# 1582    17-10--1903
# 1631              -
# 1666      01-7-1897
# 1804      01-081904
# 1879       17-02-??

df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('07-081891', '07-08-1891')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('0608-1906', '06-08-1906')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('17-10--1903', '17-10-1903')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('01-7-1897', '01-07-1897')
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('01-081904', '01-08-1904')

# when converting to date, I also found this illegal date. removing it.
df['vertrekDatumCl'] = df['vertrekDatumCl'].replace('29-02-1902', 'xx-xx-1902')


# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['vertrekDatumCl'] = df['vertrekDatumCl'][df['vertrekDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]

# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD
df['vertrekDatumCl'] = pd.to_datetime(df['vertrekDatumCl'], format='%d-%m-%Y', errors='coerce').dt.strftime('%Y-%m-%d')


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
x = df['geboorteDatum'][~df['geboorteDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(x.dropna())

# below is output of 'wrong' values and 'suggested corrections' after '//'
#178               02-05-1859
#254                 10-05-??
#265              02-12-11864
#428     06-05-1878hARDERWIJK
#430                0709-1852
#438              20-04-1882
#500              15-02-1874
#655                 leesbaar
#674              04-11-1881
#760                    29112
#883               10-04-????
#899              28-09-18877
#938                     1702
#1051             06--11-1863
#1141              19-0301885
#1368               27-08-???
#1376               0912-1880
#1484              16-02-187?
#1507              20-08-1180
#1768                 16-04-?
#1777               2-05-1877
#1879               22-04- ??

# pickup trailing spaces
df['geboorteDatumCl'] = df['geboorteDatumCl'].str.strip()


df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('02-05-1859', '02-05-1859')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('02-12-11864', '02-12-1864')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('06-05-1878hARDERWIJK', '06-05-1878')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('0709-1852', '07-09-1852')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('06--11-1863', '06-11-1863')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('19-0301885', '19-03-1885')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('0912-1880', '09-12-1880')
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('20-08-1180', '20-08-1880')

# found later this case as well
df['geboorteDatumCl'] = df['geboorteDatumCl'].replace('36-07-1863', '26-07-1863')



y = df['geboorteDatum'][~df['geboorteDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(y.dropna())
#254        10-05-??
#655        leesbaar
#760           29112
#883      10-04-????
#899     28-09-18877
#938            1702
#1368      27-08-???
#1484     16-02-187?
#1768        16-04-?
#1777      2-05-1877
#1879      22-04- ??
# Name: geboorteDatum, dtype: object


# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['geboorteDatumCl'] = df['geboorteDatumCl'][df['geboorteDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]


# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD (originally resulted in error on this date: 36-07-1863, fixed above)
df['geboorteDatumCl'] = pd.to_datetime(df['geboorteDatumCl'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')


#############################################
#                                           #
# burgerLinker familynames without prefixes #
#                                           #
#############################################

df['familienaamCl'] = df['familienaam'].str.split(',').str[0]
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Vernes/Venes.*$)', 'Vernes')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^H. Vaillard.*$)', 'Vaillard')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Schöttelndreier.*$)', 'Schottelndreier')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Mots\. De.*$)', 'Mots')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(.\(.*$)', '')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(.\[.*$)', '')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'( \- )', '')

df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Op de bladen.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Op blad.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Op dit blad.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Eerste gedeelte.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Niets vermeld.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^naam op de laatste regel is.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Blad 89 ontbreekt.*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^N\.N\..*$)', 'xxx')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(^Leeg.*$)', 'xxx')

df['familienaamCl'] = df['familienaamCl'].replace('xxx', np.nan) # somewhat ugly, but wasn't able to set to nan right away

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


df['familienaamCl'] = df['familienaamCl'].astype(str)
# bug in pandas -> has created 'nan'-string of NaN (missing values) fixing later on

df['familienaamCl'] = (df['familienaamCl'].str.lower()
                                    .str.strip() 
                                    .map(lambda x: unidecode.unidecode(x)) )
df['familienaamCl'] = df['familienaamCl'].str.replace(r' ', '')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'\.', '')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(?i)ch', 'g') #(?i) ignores case
df['familienaamCl'] = df['familienaamCl'].str.replace(r'([Cc])', 'k') # either capital C or regular c
df['familienaamCl'] = df['familienaamCl'].str.replace(r'([Zz])', 's')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(?i)ph', 'f')
df['familienaamCl'] = df['familienaamCl'].str.replace(r'(?i)ij', 'y')
df['familienaamCl'] = df['familienaamCl'].replace('nan', '') # should be fixed in pandas 2.4

df['voornaamCl'] = df['voornaam'].astype(str) # bug in pandas NaN is converted to nan
df['voornaamCl'] = (df['voornaamCl'].str.lower()
                                    .str.strip() 
                                    .map(lambda x: unidecode.unidecode(x)) )
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
df['registrationId'] = 'NAH940-DBRegister-1888-1909-' + df['regel'].astype(str)

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
dfBak.to_csv("../data/derived/db1888_1909_clean.csv", index = False)

# write abridged .csv file for burgerLinker
dfBurgerLinker = df[['registrationId', 'personId','geboorteDatumCl', 'familienaamCl','voornaamCl']]
dfBurgerLinker.to_csv("../data/derived/db1888_1909_clean_unique.csv", index = False)

# write abridged .csv file for NRCM workshop (with new var names and adding birth place variable)
dfNRCM = df[['registrationId', 'personId','geboorteDatumCl','familienaamCl','voornaamCl', 'geboortePlaats']]
dfNRCM = dfNRCM.rename(columns={'geboorteDatumCl': 'birthDate', 'familienaamCl': 'familyName', 
       'voornaamCl': 'givenName', 'geboortePlaats': 'birthPlace'})

dfNRCM.to_csv("../data/derived/db1888_1909_clean_unique_NCRM.csv", index = False)



