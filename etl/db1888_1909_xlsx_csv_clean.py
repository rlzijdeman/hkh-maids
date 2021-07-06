import pandas as pd
import numpy as np 

# read in excel file
df = pd.read_excel("../data/source/NAH inv 940 dienstboderegister 1888-1909.xlsx", dtype='str', na_values='---')

# add more informative and 'clean' column names
df.columns = ['regel', 'datumInschrijving', 'familienaam', 'voornaam', 'geboorteDatum', 'geboortePlaats',
       'burgerlijkeStaat', 'religie', 'beroep', 'verblijf', 'aankomstDatum',
       'vorigeWoonplaats', 'vertrekDatum', 'vertrekPlaats', 'opmerkingen', 'blad']


#print(df)

# now go through burgerLinker data cleaning steps
# https://github.com/CLARIAH/burgerLinker/wiki/01.-Data-standardization

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


# write out as .csv file
df.to_csv("../data/derived/db1888_1909_clean.csv")
