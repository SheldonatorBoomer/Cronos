import requests
import re
import uuid

def scrapeUrl(targetUrl):
    dataStore = []
    try:
        # Ensure URL starts with http:// or https://
        if not targetUrl.startswith("http"):
            if targetUrl.startswith("www"):
                 # Add http:// if the URL starts with "www"
                targetUrl = "http://" + targetUrl
            else:
                raise ValueError("URL must start with http or https")


        # Make the HTTPS request with timeout - We may want to increase the timeout with random timer and probably a smarter implementation
        r = requests.get(targetUrl, timeout=10)
        # Raises HTTPError for bad responses (4xx, 5xx)
        r.raise_for_status()

        # Grab the targetUrl html
        extractedData = r.text
        dataStore.append(targetUrl)

        # Website name
        domain_part = targetUrl.split("//", 1)[-1].split("/", 1)[0]
        domain_clean = domain_part.replace("www.", "").split(".")[0]
        dataStore.append(domain_clean)

        # UUID
        namespace = uuid.NAMESPACE_DNS
        hashed = str(uuid.uuid5(namespace, targetUrl))
        dataStore.append(hashed)

        # Extract <title>
        pattern_title = r'<title\b[^>]*>\s*(.*?)\s*</title>'
        title = re.findall(pattern_title, extractedData, re.IGNORECASE | re.DOTALL)
        dataStore.append(title if title else "No title found")

        # Extract hrefs - This will help us get more pages to explore (Regex)
        pattern_href = r'''
          href\s*=\s*
          (?:
            "([^"]*)"
            | '([^']*)'
            | ([^>\s]+)
          )
        '''
        flags = re.IGNORECASE | re.VERBOSE
        matches = re.findall(pattern_href, extractedData, flags=flags)

        # Normalising our links to ensure minimal errors - We could make this easier to avoid any files for example css / pdf.
        addressUrl = domain_part

        scrapedUrls = []
        # Looping through our regex matches
        for match in matches:
            url = match[0] or match[1] or match[2]
            url = url.strip()
            # If there is a link that isn't part of this domain then skip - Normally you would continue to look at other domains. This is needed to make a search engine.
            if not url:
                continue
            if addressUrl in url:
                scrapedUrls.append(url)
            elif url.startswith("/"):
                # Ensuring that the full URL is used.
                scrapedUrls.append(f"https://{addressUrl}{url}")

        dataStore.append(scrapedUrls)

    except Exception as e:
        # Returns error - This helps the crawler script to move on
        print(f"[ERROR] Failed to scrape '{targetUrl}': {e}")
        return None
    # Returns the data collected if successful
    return dataStore
