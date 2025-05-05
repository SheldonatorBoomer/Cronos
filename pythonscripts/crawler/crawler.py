import sqlite3
from scrapeurl import scrapeUrl
from datetime import datetime

# Connect to a database
conn = sqlite3.connect("../database/Cronos.db")
# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create a list of seed sites. This example is of BBC
Seeds = ["https://www.bbc.co.uk/","https://www.bbc.co.uk/news/articles/cj45r14w99eo","https://www.bbc.co.uk/search?q=lamine+yamal&d=NEWS_PS"]

def Crawl(Seeds):
    # Function for going through the seeds and obtaining more links
    for seed in Seeds:
        # Shows the site that we are looking at
        print(seed)
        # Check if the URL already exists in our database
        cursor.execute("SELECT * FROM Sites WHERE url = ?", (seed,))
        URL = cursor.fetchone()
        if not URL:
            # Use our Scrape URL script to look at this specific url and return hashes, page title and links found
            r = scrapeUrl(seed)
            # Check if r is None before accessing r[4] - R is short for return
            if r is None:
                print(f"Failed to scrape {seed}. Skipping this URL.")
                # Skip this URL and continue to the next one
                continue

            # Ensure r[4] is not None before proceeding
            if r[4]:
                # Going through the returned links and ensure we are not creating duplicates
                for link in r[4]:
                    cursor.execute("SELECT * FROM Sites WHERE url = ?", (link,))
                    URL = cursor.fetchone()
                    if not URL:
                        # Not a duplicate. Add to CrawlerToDO
                        cursor.execute("""
                            INSERT INTO CrawlerToDo (url)
                            VALUES (:url)
                            ON CONFLICT(url) DO NOTHING
                        """, {'url': link})
            else:
                print(f"No links found for {seed}")

            # UPDATE / INSERT to Sites table. Means we gathered enough data to search
            # Ensure valid title
            title = r[3][0] if r[3] and r[3][0] else "No title found"
            cursor.execute("""
                INSERT INTO Sites (urlHash, url, title)
                    VALUES (:urlHash, :url, :title)
                    ON CONFLICT(urlHash) DO UPDATE SET
                        urlHash = excluded.urlHash,
                        url = excluded.url,
                        title = excluded.title
                """, {'urlHash': r[2], 'url': r[0], 'title': title})
            conn.commit()

            # UPDATE / INSERT Crawler - Important for future features to use the lastchecked columns
            cursor.execute("""
                INSERT INTO Crawler (urlHash, url, lastChecked)
                VALUES (:urlHash, :url, :lastChecked)
                ON CONFLICT(urlHash) DO UPDATE SET
                    urlHash = excluded.urlHash,
                    url = excluded.url,
                    lastChecked = excluded.lastChecked
            """, {'urlHash': r[2], 'url': r[0], 'lastChecked': datetime.today().strftime('%d-%m-%Y')})
            conn.commit()

            # Preparing data for indexing
            if title != "No title found":  # Only process text if title is valid
                # Preparing the title and create Tokens
                Tokens = title.lower().split(" ")
                for token in Tokens:
                    # Check if this token exists in our terms table
                    cursor.execute("SELECT * FROM Terms WHERE term = ?", (token,))
                    conn.commit()
                    row = cursor.fetchone()
                    if row:
                        # Exists - We need to update the row - Get the ID
                        rowId = row[0]
                        # Check if our urlHash exists in the string
                        if r[2] in row[2]:
                            print("Found match!")
                        else:
                            # We need to update this row
                            nurlHash = row[2] + "," + r[2]
                            cursor.execute("UPDATE Terms SET urlHash = ? WHERE termId = ?", (nurlHash, rowId))
                            conn.commit()
                    else:
                        # Doesn't exist - Insert Query
                        cursor.execute("""
                            INSERT INTO Terms (term, urlHash, position)
                            VALUES (?, ?, ?)
                        """, (token, r[2], 0))

                        cursor.execute("""
                        SELECT * FROM Terms WHERE term = ?
                        """, (token,))

                        row = cursor.fetchone()
                        rowId = row[0]

    # Check the CrawlerToDo table and recurse if necessary
    cursor.execute("SELECT url FROM CrawlerToDo")
    rows = cursor.fetchall()
    # Quick rows to urls
    urls = [row[0] for row in rows]
    # We need to clear the Todo as we have already loaded all the URLS to seed
    cursor.execute("DELETE FROM CrawlerToDo")
    if not urls:
        # This means our script has finished and there isn't any new links to explore within all of our seeded websites
        print("Finished!")
    else:
        # recursion
        Crawl(urls)



# Initiate the crawling process with the seeds
Crawl(Seeds)
# Database Connect commit and close
conn.commit()
conn.close()
