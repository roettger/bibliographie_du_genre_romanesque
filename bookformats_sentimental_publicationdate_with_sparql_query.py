from scipy.stats import chi2_contingency
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL-Abfrage als String
sparql_query = """
    prefix mmd:<http://data.mimotext.uni-trier.de/entity/>
    prefix mmdt:<http://data.mimotext.uni-trier.de/prop/direct/> 
    SELECT (str(SAMPLE(year(?date))) as ?year) (count(?format) as ?count) ?format 
    WHERE {
        ?item mmdt:P26 ?format.
        ?item mmdt:P36 mmd:Q3085 . #item about sentimentalism
        ?item mmdt:P9 ?date .
        FILTER(lang(?format) = "fr")
        BIND(str(year(?date)) as ?year)
        SERVICE wikibase:label {bd:serviceParam wikibase:language "en" .}
    }
    GROUP BY ?format ?year ?count
"""

# Verbindung zur SPARQL-Endpunkt herstellen
sparql = SPARQLWrapper("https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)

# Ausführen der SPARQL-Abfrage und Erhalt der Ergebnisse
results = sparql.query().convert()

# Verarbeiten der Ergebnisse
observed_data = []
for result in results["results"]["bindings"]:
    year = result["year"]["value"]
    count = int(result["count"]["value"])
    book_format = result["format"]["value"]
    observed_data.append([year, count, book_format])

# Konvertiere die Daten in ein Format, das von chi2_contingency erwartet wird
format_counts = {}
years = set()
for year, count, book_format in observed_data:
    years.add(year)
    if book_format not in format_counts:
        format_counts[book_format] = {}
    format_counts[book_format][year] = count

# Fülle fehlende Werte mit 0 auf
for book_format in format_counts:
    for year in years:
        if year not in format_counts[book_format]:
            format_counts[book_format][year] = 0

# Sortiere die Jahre
years = sorted(list(years))

# Konvertiere zu einer Liste für die Verwendung in chi2_contingency
data_list = []
for book_format, year_counts in format_counts.items():
    data_list.append([year_counts[year] for year in years])

# Führe den Chi-Quadrat-Test durch
chi2, p, dof, expected = chi2_contingency(data_list)

print("Chi-Quadrat-Wert:", chi2)
print("p-Wert:", p)
print("Freiheitsgrade:", dof)
print("Erwartete Frequenzen:")
for row in expected:
    print(row)
