import pandas as pd
from scipy.stats import chi2_contingency

# Daten einlesen
data = {
    'year': [1751, 1751, 1751, 1751, 1751, 1751, 1751, 1751, 1751, 1751, 1752, 1752, 1752, 1752, 1752, 1752, 1753, 1753, 1753, 1753, 1753, 1753],
    'format': ['in-12', 't. in-12', 'part, in-8', 'part, in-12', '4 t. in-12', '2 part, in-8', '2 part, in-12', 'in-8', 'part, in-12', 'in-12', '2 part, in-8', '2 t. in-8', '4 part, in-12', '4 part, in-12', 'in-8', 'in-12', '2 t. in - 12', '2 t. in-12', '3t. in-12', '4 t. in-12', '6 part, in-12', '6 t. in-12']
}

df = pd.DataFrame(data)

# Format in-8, in-12, in-18 bestimmen
def determine_format(format_str):
    if 'in-8' in format_str:
        return 'in-8'
    elif 'in-12' in format_str:
        return 'in-12'
    elif 'in-18' in format_str:
        return 'in-18'
    else:
        return None

df['format'] = df['format'].apply(determine_format)

# Kreuztabelle erstellen
crosstab = pd.crosstab(df['year'], df['format'])

# Chi-Quadrat-Unabhängigkeitsprüfung durchführen
chi2, p, dof, expected = chi2_contingency(crosstab)

# Ergebnis ausgeben
print("Chi-Quadrat-Wert:", chi2)
print("p-Wert:", p)
print("Freiheitsgrade:", dof)
print("Erwartete Frequenzen:\n", expected)
