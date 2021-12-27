# INFO216-Knowledge-Graphs
Knowledge graph course spring 2021 at the University of Bergen.


## File information:

- [program and data](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/tree/main/program%20and%20data) folder containing the program and data, folder usefull to keep project structure and file pathing errors to a minimum.

  - [program](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/blob/main/program%20and%20data/program.py) is the python project containing the code and     program.  

  - [fylker2](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/blob/main/program%20and%20data/fylker2.csv) is a csv file containing data about counties.  

  - [kommuner1](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/blob/main/program%20and%20data/kommuner1.csv) is a csv file containing data about            municipalities.  

- [Info216ProjectReport_167,189](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/blob/main/Info216ProjectReport_167%2C189.pdf) is a pdf containing my group's project report describing both how we worked on this project, as well as detailed information about issues we had while working on it, as well as findings when we finished the work.

## About the assignment:

Full description of this project can be found at the [course wiki](https://wiki.uib.no/info216/index.php/About_the_group_project).

This was a very open assignment where the main goal was to develop a semantic knowledge graph based (RDF, SPARQL, OWL...) dataset, application, or service. We chose to create an application for seeking information about counties, municipalities as well as the population of different municipalities in Norway. Information about counties and municipalities is fetched locally by downloading the information from SSB. Information about population is gathered from Wikidata by using SPARQLWrapper.

## How to run the program:
To start the program you need to create a new project in PyCharm (or your preferred IDE), and open the folder named [program and data](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/tree/main/program%20and%20data). This folder contains the [code](https://github.com/bernardstensaker/INFO216-Knowledge-Graphs/blob/main/program%20and%20data/program.py) as a python file, as well as two smaller datasets in .csv format we downloaded from SSB [(1) counties](https://www.ssb.no/en/klass/klassifikasjoner/104), [(2) municipalities](https://www.ssb.no/klass/klassifikasjoner/131). It is essential for the program to run correctly that these three files are in the same folders, as the file pathing would otherwise create errors.

After this, make sure you have a working programming environment, if not create a new one and most importantly make sure you have all the packages installed listed under libraries below.

## Built using:

### Languages:

- Python

### Libraries:

- RDFlib

- RDFlib-jsonld

- Pandas

- SPARQLWrapper
