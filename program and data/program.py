from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import XSD
import pandas as pd
from rdflib.plugins.sparql import prepareQuery
from SPARQLWrapper import SPARQLWrapper, JSON

# Lage grafen og definere namespaces

g = Graph()

dbp = Namespace("https://dbpedia.org/page/")
dbo = Namespace("https://dbpedia.org/ontology/")
wiki = Namespace("https://www.wikidata.org/wiki/")
prop = Namespace(wiki + "Property:")

# binde namespaces til grafen

g.bind("dbp", dbp)
g.bind("dbo", dbo)
g.bind("wiki", wiki)
g.bind("prop", prop)

# les csv fil

csv_fylker = pd.read_csv("fylker2.csv", encoding="utf-8", delimiter=";")
csv_kommuner = pd.read_csv("kommuner1.csv", encoding="utf-8", delimiter=";")

# droppe unødvendige og tomme rader


def drop_rows(csv_file):
    csv_file.drop(["parentCode", "level", "validFrom", "validTo", "shortName", "notes"], axis=1, inplace=True)


drop_rows(csv_fylker)
drop_rows(csv_kommuner)

# fikse strengene så det blir gyldig URI

csv_fylker = csv_fylker.replace(to_replace="-", value=" ", regex=True)
csv_fylker = csv_fylker.replace(to_replace=" ", value="_", regex=True)

csv_kommuner = csv_kommuner.replace(to_replace="-", value=" ", regex=True)
csv_kommuner = csv_kommuner.replace(to_replace=" ", value="_", regex=True)

# legge inn fylker og kommuner i graf

for index, row in csv_fylker.iterrows():
    name = row['name']
    g.add((URIRef(dbp + name), URIRef(wiki + "Q21503252"), URIRef(dbo + "county")))
for index, row in csv_kommuner.iterrows():
    name = row['name']
    g.add((URIRef(dbp + name), URIRef(wiki + "Q21503252"), URIRef(dbo + "municipality")))

# lag tomme lister for hvert fylke

Oslo, Rogaland, Møre_og_Romsdal, Nordland, Viken, Innlandet, Vestfold_og_Telemark, Agder, Vestland, Trøndelag, Troms_og_Finnmark = ([] for i in range(11))

# dele opp kommunene og legge de i tomme listene


def del_kommuner(csv_file):
    for index, row in csv_file.iterrows():
        name = row['name']
        code = row['code']
        code = str(code)
        if code == '301':
            Oslo.append(name)
        elif code[:2] == '11':
            Rogaland.append(name)
        elif code[:2] == '15':
            Møre_og_Romsdal.append(name)
        elif code[:2] == '18':
            Nordland.append(name)
        elif code[:2] == '30':
            Viken.append(name)
        elif code[:2] == '34':
            Innlandet.append(name)
        elif code[:2] == '38':
            Vestfold_og_Telemark.append(name)
        elif code[:2] == '42':
            Agder.append(name)
        elif code[:2] == '46':
            Vestland.append(name)
        elif code[:2] == '50':
            Trøndelag.append(name)
        elif code[:2] == '54':
            Troms_og_Finnmark.append(name)
        else:
            pass


del_kommuner(csv_kommuner)

# lage en dict med key=fylke og value=liste av kommuner

alle = {}


def lag_dict():
    alle['Oslo'] = Oslo
    alle['Rogaland'] = Rogaland
    alle['Møre_og_Romsdal'] = Møre_og_Romsdal
    alle['Nordland'] = Nordland
    alle['Viken'] = Viken
    alle['Innlandet'] = Innlandet
    alle['Vestfold_og_Telemark'] = Vestfold_og_Telemark
    alle['Agder'] = Agder
    alle['Vestland'] = Vestland
    alle['Trøndelag'] = Trøndelag
    alle['Troms_og_Finnmark'] = Troms_og_Finnmark


lag_dict()

# koble sammen fylker og kommuner i grafen

for k, v in alle.items():
    for value in v:
        g.add((URIRef(dbp + value), URIRef(prop + "P131"), URIRef(dbp + k)))

for k, v in alle.items():
    for value in v:
        g.add((URIRef(dbp + k), URIRef(prop + "P150"), URIRef(dbp + value)))

# søk for å finne bestemt fylke en kommune ligger i


def find_fylke(municipality):
    municipality = URIRef(dbp + municipality)
    q = prepareQuery(
        """
        PREFIX prop: <https://www.wikidata.org/wiki/Property:>
        SELECT ?county WHERE {
        ?municipality prop:P131 ?county.
        }
        """)
    capital_result = g.query(q, initBindings={'municipality' : municipality})

    for row in capital_result:
        print(row)

# søk for å liste alle kommuner i et fylke


def find_kommune(county):
    county = URIRef(dbp + county)
    q = prepareQuery(
        """
        PREFIX prop: <https://www.wikidata.org/wiki/Property:>
        SELECT ?municipality WHERE { 
        ?county prop:P150 ?municipality.
        }
        """)
    capital_result = g.query(q, initBindings={'county' : county})

    for row in capital_result:
        print(row)

# hente innbyggertall fra wikidata og bruke to dicts for å formatere informasjonen etterpå:


x = {}
y = {}

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

sparql.setQuery("""
    SELECT ?s ?sLabel ?population WHERE
    {
    ?s wdt:P31 wd:Q755707.
    OPTIONAL { ?s wdt:P1082 ?population. }

    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }


""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    x[result["sLabel"]["value"]] = result["population"]["value"]

for k, v in x.items():

    k = k.replace(" Municipality", "")
    y[k] = v


# legg inn innbyggertall i grafen

for k, v in y.items():
    k = str(k.replace(" ", "_"))
    k = str(k.replace("-", "_"))

    g.add((URIRef(dbp + k), URIRef(dbo + "populationTotal"), Literal(v, datatype=XSD.integer)))


def hent_innbyggertall(kommune):
    for k, v in y.items():
        if kommune in k:
            print(kommune, "kommune har", v, "innbyggere.")

# startmeny for de forskjellige søkene


def meny():
    print("----------------------------------------")
    print("1 = vis alle kommuner i bestemt fylke")
    print("2 = vis hvilket fylke bestemt kommune ligger i")
    print("3 = vis innbyggertall i bestemt kommune")
    print("x - stop programmet")
    print("---------------------------------------- \n")
    x = input("Hva vil du gjøre? ")
    if x == "1":
        print("----------------------------------------")
        return ask1()
    elif x == "2":
        print("----------------------------------------")
        return ask2()
    elif x == "3":
        print("----------------------------------------")
        return ask3()
    elif x == "x":
        print("Thank you for visiting, please come again")
        return
    else:
        print("\n ugyldig valg \n")
        return meny()

# refererer til uthenting av liste av kommuner ovenfor, med litt ekstra steg for å sørge for at skrivefeil ikke
# fører til feil


def ask1():
    question = input("skriv inn fylke eller skriv X for meny: ")
    question = question.replace(" ", "_")

    question = ' '.join(word[0].upper() + word[1:] for word in question.split())

    if question in alle.keys():
        find_kommune(question)
        print(" ")
        return ask1()
    elif question == "X":
        return meny()
    else:
        print("ugyldig valg")
        return ask1()

# refererer til uthenting hvilket fylke en kommune er i ovenfor, med litt ekstra steg for å sørge for at skrivefeil ikke
# fører til feil


def ask2():
    question = input("Skriv inn kommune eller skriv X for meny: ")
    question = question.replace("-", "_")
    question = question.replace(" ", "_")
    question = ' '.join(word[0].upper() + word[1:] for word in question.split())
    alle_liste = []
    for v in alle.values():
        for value in v:
            alle_liste.append(value)

    if question in alle_liste:
        find_fylke(question)
        return ask2()
    elif question == 'X':
        return meny()
    else:
        print("ugyldig valg")
        return ask2()

# refererer til uthenting innbyggertall i en kommune, med litt ekstra steg for å sørge for at skrivefeil ikke
# fører til feil


def ask3():
    question = input("Skriv inn kommune eller skriv X for meny: ")
    question = ' '.join(word[0].upper() + word[1:] for word in question.split())

    if question in y.keys():
        hent_innbyggertall(question)
        return ask3()
    elif question == "X":
        return meny()
    else:
        print("ugyldig valg")
        return ask3()

# for å starte programmet:


meny()

# for å inspisere hele grafen (fjern # fra linjen under):


# print(g.serialize(format="turtle").decode())