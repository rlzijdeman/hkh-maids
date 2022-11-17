import pandas as pd
import numpy as np 
from fold_to_ascii import fold # for handling diacritics and other special char stuff
import unidecode

# read in excel file
df = pd.read_excel("../data/source/NAH inv  939 dienstboderegister 1880-1887.xlsx", dtype='str', na_values='---')

# output database
#print(df)

# add more informative and 'clean' column names
df.columns = ['regel', 'datumInschrijving', 'familienaam', 'voornaam', 'geboorteDatum', 'geboortePlaats',
       'burgerlijkeStaat', 'religie', 'beroep', 'verblijf', 'aankomstDatum',
       'vorigeWoonplaats', 'vertrekDatum', 'vertrekPlaats', 'opmerkingen', 'blad']

#print(df)

################################ date of arrival ##############################

df['aankomstDatumCl'] = df['aankomstDatum'].astype(str)
#### show all dates that do not match 2digits-2digits-4digits
x = df['aankomstDatum'][~df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]
print(x.dropna())
# 53     wijk 1  blz. 75
# 54
# 64     wijk 5  blz. 69
# 70           02-101881
# 89              22-08-
# 244             15-07-
# 437    wijk 9  blz. 16
# 468        10-09--1883

df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('02-101881', '02-10-1881')


# one value is out of dd-mm-yyyy scope
df['aankomstDatumCl'] = df['aankomstDatumCl'].replace('10-16-1885', '10-xx-1885')


# ok let's kill the remaing values
#### so now only preserve values of the pattern 2digits-2digits-4digits
df['aankomstDatumCl'] = df['aankomstDatumCl'][df['aankomstDatumCl'].str.contains('^[0-9][0-9]-[0-9][0-9]-1[8-9][0-9][0-9]$')]



# now final step for dates: invert DD-MM-YYYY to YYYY-MM-DD
df['aankomstDatumCl'] = pd.to_datetime(df['aankomstDatumCl'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

print(df['aankomstDatumCl'])