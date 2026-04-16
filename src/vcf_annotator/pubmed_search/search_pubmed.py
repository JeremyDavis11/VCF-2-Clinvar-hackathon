"""Search PubMed for articles related to the variant selected by the user"""

import requests


def search_pubmed(gene_symbol, max_results=5):
    # search for articles
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": f"{gene_symbol} clinical significance",
        "retmax": max_results,
        "retmode": "json",
    }
    response = requests.get(search_url, params=params)
    pmids = response.json()["esearchresult"]["idlist"]

    # fetch abstracts
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "abstract",
        "retmode": "text",
    }
    response = requests.get(fetch_url, params=params)
    return pmids, response.text
