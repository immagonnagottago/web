import os
import re

# 1. Configure where your site folders are
SITE_DIRS = ["../site1", "../site2"]  # relative to search.py

# 2. Build inverted index
index = {}

for site in SITE_DIRS:
    if not os.path.exists(site):
        continue
    for filename in os.listdir(site):
        if filename.endswith(".md"):
            path = os.path.join(site, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().lower()
                words = re.findall(r'\w+', text)
                for word in words:
                    index.setdefault(word, set()).add(path)

# 3. Search function
def search(query):
    query_words = re.findall(r'\w+', query.lower())
    results = {}
    for word in query_words:
        for path in index.get(word, []):
            results[path] = results.get(path, 0) + 1
    # Rank by number of matching words
    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return ranked

# 4. Command-line interface
if __name__ == "__main__":
    while True:
        q = input("Search> ")
        if q.strip().lower() in ["exit", "quit"]:
            break
        results = search(q)
        if not results:
            print("No results found.")
        else:
            print("Results:")
            for path, score in results:
                print(f"{path} (score: {score})")
