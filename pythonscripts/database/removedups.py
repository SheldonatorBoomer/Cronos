# This scripts removes duplicates caused by some pages having different URLS
import sqlite3
import os

print("Preparing to remove duplicates")
conn = sqlite3.connect("Cronos.db")
cursor = conn.cursor()

# Delete rows with duplicate 'title', keeping the one with the lowest rowid
cursor.execute('''
      DELETE FROM Sites
      WHERE urlHash NOT IN (
          SELECT MIN(urlHash)
          FROM Sites
          GROUP BY title
      );
''')

conn.commit()
conn.close()
print("Finished!")
