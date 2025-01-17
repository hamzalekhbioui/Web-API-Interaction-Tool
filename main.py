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
    if "items" in message:  # Multi-item response
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


def display_metadata(article):
    if "published-print" in article and "date-parts" in article["published-print"]:
        year = article["published-print"]["date-parts"][0][0]
    elif "published-online" in article and "date-parts" in article["published-online"]:
        year = article["published-online"]["date-parts"][0][0]
    else:
        year = "N/A"

    title = article.get("title", ["No Title"])[0]
    authors = ", ".join(
        f"{a.get('given', 'N/A')} {a.get('family', 'N/A')}"
        if 'given' in a and 'family' in a else "N/A"
        for a in article.get("author", [])
    )
    journal = article.get("container-title", ["N/A"])[0]
    metadata = {
        "Title": title,
        "Authors": authors,
        "Journal": journal,
        "Volume": article.get("volume", "N/A"),
        "Year": year,
        "URL": article.get("URL", "N/A"),
        "DOI": article.get("DOI", "N/A"),
        "Publisher": article.get("publisher", "N/A"),
    }

    print("\nArticle Details:")
    print("-" * 40)
    for key, value in metadata.items():
        print(f"{key:<15}: {value}")
    print("-" * 40)


if __name__ == "__main__":
    # Check for command-line arguments
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

