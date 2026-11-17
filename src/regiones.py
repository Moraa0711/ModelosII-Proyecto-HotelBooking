# Región de origen de cada código de país (ISO 3166-1 alfa-3) presente en el dataset.
# Generado con pycountry y pycountry-convert; se guarda fijo para no depender de esas librerías.
# Portugal se trata aparte (país de los hoteles). Los códigos que no son estándar (CN, TMP, ATA, ATF, UMI)
# y cualquier código nuevo van a 'Otros'; los faltantes, a 'Desconocido'.
REGIONES = {
    "ABW": "América del Norte", "AIA": "América del Norte", "BHS": "América del Norte", "BRB": "América del Norte", "CRI": "América del Norte", "CUB": "América del Norte", "CYM": "América del Norte", "DMA": "América del Norte", "DOM": "América del Norte", "GLP": "América del Norte",
    "GTM": "América del Norte", "HND": "América del Norte", "JAM": "América del Norte", "KNA": "América del Norte", "LCA": "América del Norte", "MEX": "América del Norte", "NIC": "América del Norte", "PAN": "América del Norte", "PRI": "América del Norte", "SLV": "América del Norte",
    "USA": "América del Norte", "VGB": "América del Norte",
    "ARG": "América del Sur", "BOL": "América del Sur", "BRA": "América del Sur", "CHL": "América del Sur", "COL": "América del Sur", "ECU": "América del Sur", "GUY": "América del Sur", "PER": "América del Sur", "PRY": "América del Sur", "SUR": "América del Sur",
    "URY": "América del Sur", "VEN": "América del Sur",
    "ARE": "Asia", "ARM": "Asia", "AZE": "Asia", "BGD": "Asia", "BHR": "Asia", "CHN": "Asia", "CYP": "Asia", "GEO": "Asia", "HKG": "Asia", "IDN": "Asia",
    "IND": "Asia", "IRN": "Asia", "IRQ": "Asia", "ISR": "Asia", "JOR": "Asia", "JPN": "Asia", "KAZ": "Asia", "KHM": "Asia", "KOR": "Asia", "KWT": "Asia",
    "LAO": "Asia", "LBN": "Asia", "LKA": "Asia", "MAC": "Asia", "MDV": "Asia", "MMR": "Asia", "MYS": "Asia", "NPL": "Asia", "OMN": "Asia", "PAK": "Asia",
    "PHL": "Asia", "QAT": "Asia", "SAU": "Asia", "SGP": "Asia", "SYR": "Asia", "THA": "Asia", "TJK": "Asia", "TUR": "Asia", "TWN": "Asia", "UZB": "Asia",
    "VNM": "Asia",
    "ALB": "Europa", "AND": "Europa", "AUT": "Europa", "BEL": "Europa", "BGR": "Europa", "BIH": "Europa", "BLR": "Europa", "CHE": "Europa", "CZE": "Europa", "DEU": "Europa",
    "DNK": "Europa", "ESP": "Europa", "EST": "Europa", "FIN": "Europa", "FRA": "Europa", "FRO": "Europa", "GBR": "Europa", "GGY": "Europa", "GIB": "Europa", "GRC": "Europa",
    "HRV": "Europa", "HUN": "Europa", "IMN": "Europa", "IRL": "Europa", "ISL": "Europa", "ITA": "Europa", "JEY": "Europa", "LIE": "Europa", "LTU": "Europa", "LUX": "Europa",
    "LVA": "Europa", "MCO": "Europa", "MKD": "Europa", "MLT": "Europa", "MNE": "Europa", "NLD": "Europa", "NOR": "Europa", "POL": "Europa", "ROU": "Europa", "RUS": "Europa",
    "SMR": "Europa", "SRB": "Europa", "SVK": "Europa", "SVN": "Europa", "SWE": "Europa", "UKR": "Europa",
    "ASM": "Oceanía", "AUS": "Oceanía", "FJI": "Oceanía", "KIR": "Oceanía", "NCL": "Oceanía", "NZL": "Oceanía", "PLW": "Oceanía", "PYF": "Oceanía",
    "AGO": "África", "BDI": "África", "BEN": "África", "BFA": "África", "BWA": "África", "CAF": "África", "CIV": "África", "CMR": "África", "COM": "África", "CPV": "África",
    "DJI": "África", "DZA": "África", "EGY": "África", "ETH": "África", "GAB": "África", "GHA": "África", "GNB": "África", "KEN": "África", "LBY": "África", "MAR": "África",
    "MDG": "África", "MLI": "África", "MOZ": "África", "MRT": "África", "MUS": "África", "MWI": "África", "MYT": "África", "NAM": "África", "NGA": "África", "RWA": "África",
    "SDN": "África", "SEN": "África", "SLE": "África", "STP": "África", "SYC": "África", "TGO": "África", "TUN": "África", "TZA": "África", "UGA": "África", "ZAF": "África",
    "ZMB": "África", "ZWE": "África",
}
