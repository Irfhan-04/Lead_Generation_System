from Bio import Entrez

Entrez.email = "your_email@example.com"

def fetch_recent_publications(author_name: str, max_results=5):
    query = f'{author_name}[Author]'
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        sort="pub date"
    )
    results = Entrez.read(handle)
    handle.close()

    return results.get("IdList", [])

def fetch_abstract(pubmed_id: str) -> str:
    handle = Entrez.efetch(
        db="pubmed",
        id=pubmed_id,
        rettype="abstract",
        retmode="text"
    )
    abstract = handle.read()
    handle.close()
    return abstract
