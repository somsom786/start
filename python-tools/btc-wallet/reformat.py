import json

# Load bitinfo_matches.json
with open("bitinfo_matches.json", "r") as f:
    matches = json.load(f)

# Reformat each entry to the new string format
reformatted = {
    match["matched_address"]: f'Strategy {match["actual_btc"]} BTC'
    for match in matches
}

# Save to a new JSON file
with open("bitinfo_reformatted.json", "w") as f:
    json.dump(reformatted, f, indent=4)

print("✅ Saved as bitinfo_reformatted.json with 'Strategy' added.")
