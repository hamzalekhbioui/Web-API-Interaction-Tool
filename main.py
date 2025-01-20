import requests
import json
import sys

def fetch_article(query_type, query_value):
    base_url = "https://api.crossref.org/works"
    if query_type == "doi":
        url = f"{base_url}/{query_value}"
    else:
        url = f"{base_url}?query.{query_type}={query_value}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error occurred: {err}")
    return None


def process_results(results):
    message = results['message']
    if "items" in message:  
        items = message["items"]
        if len(items) > 1:
            print("Multiple articles found:")
            for i, item in enumerate(items, 1):
                title = item.get("title", ["No Title"])[0]
                authors = ", ".join(
                    f"{a.get('given', 'N/A')} {a.get('family', 'N/A')}"
                    if 'given' in a and 'family' in a else "N/A"
                    for a in item.get("author", [])
                )
                print(f"{i}. {title} by {authors}")

            choice = int(input("Choose the correct article (number): ")) - 1
            return items[choice]
        elif len(items) == 1:
            return items[0]
    else:
        return message




def generate_bibtex(article):
    title = article.get("title", ["No Title"])[0]
    authors = " and ".join(
        f"{a.get('family', 'N/A')}, {a.get('given', 'N/A')}"
        if 'given' in a and 'family' in a else "N/A"
        for a in article.get("author", [])
    )
    journal = article.get("container-title", ["N/A"])[0]
    year = article.get("published-print", {}).get("date-parts", [[None]])[0][0] or \
           article.get("published-online", {}).get("date-parts", [[None]])[0][0] or "N/A"
    volume = article.get("volume", "N/A")
    pages = article.get("page", "N/A")
    doi = article.get("DOI", "N/A")
    return f"""@article{{{doi.replace('/', '_')},
    author = {{{authors}}},
    title = {{{title}}},
    journal = {{{journal}}},
    year = {{{year}}},
    volume = {{{volume}}},
    pages = {{{pages}}},
    doi = {{{doi}}}
}}"""


def display_metadata(article):
    year = article.get("published-print", {}).get("date-parts", [[None]])[0][0] or \
           article.get("published-online", {}).get("date-parts", [[None]])[0][0] or "N/A"
    title = article.get("title", ["No Title"])[0]
    authors = ", ".join(
        f"{a.get('given', 'N/A')} {a.get('family', 'N/A')}"
        if 'given' in a and 'family' in a else "N/A"
        for a in article.get("author", [])
    )
    journal = article.get("container-title", ["N/A"])[0]
    pages = article.get("page", "N/A")
    volume = article.get("volume", "N/A")
    doi = article.get("DOI", "N/A")
    bibtex = generate_bibtex(article)
    metadata = {
        "Title": title,
        "Authors": authors,
        "Journal": journal,
        "Volume": volume,
        "Pages": pages,
        "Year": year,
        "URL": article.get("URL", "N/A"),
        "DOI": doi,
        "BibTeX Key": bibtex,
    }
    print("\nArticle Details:")
    print("-" * 40)
    for key, value in metadata.items():
        print(f"{key:<15}: {value}")
    print("-" * 40)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: main.py <query_type> <query_value>")
        sys.exit(1)

    query_type = sys.argv[1].strip().lower()
    query_value = sys.argv[2].strip()

    results = fetch_article(query_type, query_value)
    if results and results.get('status') == "ok":
        article = process_results(results)
        display_metadata(article)
    else:
        print("No results found or an error occurred.")
