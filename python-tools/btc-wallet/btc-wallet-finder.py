from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time

# Load wallets.json
with open("wallets.json", "r") as f:
    local_wallets = json.load(f)

# Flatten wallet data to (prefix, rounded_btc) pairs
wallet_targets = []
for entry in local_wallets:
    prefix = entry[0]
    btc_amount = float(entry[3])  # 4th item in list is BTC string
    wallet_targets.append((prefix, round(btc_amount)))

def scrape_and_match(page_number):
    url = f"https://bitinfocharts.com/top-100-richest-bitcoin-addresses-{page_number}.html"
    print(f"\n🌐 Scraping page {page_number}")
    matches = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Wait for table
        page.wait_for_selector("table", timeout=20000)

        # Get all table rows (ignore the first header row)
        rows = page.query_selector_all("table tr")[1:]
        print(f"📄 Found {len(rows)} total rows")

        for row in rows:
            cols = row.query_selector_all("td")
            if len(cols) < 3:
                continue

            # Get address and BTC balance
            address = cols[1].inner_text().strip()
            balance_str = cols[2].inner_text().strip().replace(",", "").split(" ")[0]

            try:
                btc_value = float(balance_str)
            except ValueError:
                continue

            btc_rounded = round(btc_value)

            # Check against local wallet prefixes
            for prefix, target_rounded in wallet_targets:
                if prefix in address and btc_rounded == target_rounded:
                    print(f"✅ MATCH: {address} → {btc_value} BTC (prefix: {prefix})")
                    matches.append({
                        "prefix": prefix,
                        "matched_address": address,
                        "actual_btc": btc_value,
                        "page": page_number
                    })

        browser.close()
    return matches

if __name__ == "__main__":
    all_matches = []
    for page_to_scrape in range(3, 101):  # From page 3 to 100
        results = scrape_and_match(page_to_scrape)
        all_matches.extend(results)

    print(f"\n✅ Found {len(all_matches)} total matches.")
    with open("bitinfo_matches.json", "w") as out:
        json.dump(all_matches, out, indent=4)
    print("💾 Saved to bitinfo_matches.json")
