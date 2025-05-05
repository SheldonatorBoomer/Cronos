import sqlite3
from collections import defaultdict
import sys
import json
import re
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Join relative path to get full absolute path
db_path = os.path.join(script_dir, '..', '..', '..', 'pythonscripts', 'database', 'Cronos.db')

# normalize path
db_path = os.path.normpath(db_path)

def search(userQuery, db_path=db_path):

    #Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Process search terms - setting the userQuery / Query to lower case and creating tokens
    searchToken = [t.lower() for t in userQuery.split() if t.strip()]

    if not searchToken:
        print("No valid search terms")
        conn.close()
        return

    # Find urlHashs matching ANY term / Token
    hash_counts = defaultdict(int)
    unique_hashes = set()

    for term in searchToken:
        cursor.execute("SELECT urlHash FROM Terms WHERE term = ?", (term,))
        if result := cursor.fetchone():
            for url_hash in result[0].split(','):
                unique_hashes.add(url_hash)
                hash_counts[url_hash] += 1

    if not unique_hashes:
        print("No matching documents found")
        conn.close()
        return

    # Get documents with relevance scoring
    query = f"""
        SELECT url, title,
               (LENGTH(title) - LENGTH(REPLACE(LOWER(title), ' ', ''))) + 1 AS title_word_count
        FROM sites
        WHERE urlHash IN ({','.join(['?']*len(unique_hashes))})
    """
    cursor.execute(query, list(unique_hashes))

    # Calculate combined relevance score
    results = []
    for url, title, word_count in cursor.fetchall():
        title_terms = title.lower().split()
        termMatches = sum(1 for term in searchToken if term in title_terms)

        # Score formula: 60% term matches, 40% title brevity
        score = (0.6 * termMatches/len(searchToken)) + (0.4 * (1/word_count))
        results.append((url, title, score))

    # Sort by best matches first
    results.sort(key=lambda x: x[2], reverse=True)

    topResults = []
    for url, title, score in results[:20]:
        if round(score, 2) > 0.6 or re.search(userQuery, title, re.IGNORECASE):
            topResults.append({
                "url": url,
                "title": title,
                "match_confidence": round(score, 2)
            })

    # Create final JSON structure
    output = {
        "topResults": topResults
    }

    # Output JSON
    print(json.dumps(output, indent=2))

    conn.close()
# Example usage


if __name__ == "__main__":
    if '--create-indexes' in sys.argv:
        # Add index creation logic here
        pass
    elif len(sys.argv) > 1:
        query = sys.argv[1]
        search(query)  # Your existing search function
    else:
        print("No query provided")


#search_query = "Lamine Yamal"
#search(search_query)
