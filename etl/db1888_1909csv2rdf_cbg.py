import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, SDO
import urllib.parse

df=pd.read_csv('../data/derived/db1888_1909_clean.csv', sep=',')
#print(df)

g = Graph()
cbgo = Namespace('https://data.cbg.nl/ontology/')
hkh = Namespace('http://www.hkharderwijk.nl/nah/')
pnv = Namespace('https://w3id.org/pnv#')

for index, row in df.iterrows():
    g.add((URIRef(hkh+row['registrationId']), RDF.type, URIRef(cbgo+'PersonObservation')))
    g.add((URIRef(hkh+row['registrationId']), SDO.familyName, Literal(row['familienaam'], datatype=XSD.string) )) #still contains surnamePrefix
    g.add((URIRef(hkh+row['registrationId']), SDO.birthDate, Literal(row['geboorteDatumCl'], datatype=XSD.date) ))
    g.add((URIRef(hkh+row['registrationId']), SDO.occupation, Literal(row['beroep'], lang='nl') ))
    g.add((URIRef(hkh+row['registrationId']), URIRef(pnv+'givenName'), Literal(row['voornaam'], datatype=XSD.string) ))
    g.add((URIRef(hkh+row['registrationId']), URIRef(cbgo+'hasReligion'), Literal(row['religie'], datatype=XSD.string) ))

print(g.serialize(format='turtle'))

g.serialize('../data/derived/hkh-nah-1888-1909.ttl',format='turtle')