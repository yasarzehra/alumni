import urllib.request
import re

styles = [
    ("MasterClass", "4367b4cd-b002-4719-a418-cbce020f0d33"),
    ("Syllabus", "b78edcaa-6754-41d7-ac00-0119b41ad88a"),
    ("Genway", "a81607e2-254f-4f53-b357-68c39c9cfc03")
]

for name, uid in styles:
    url = f"https://styles.refero.design/style/{uid}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            txt = r.read().decode("utf-8", errors="ignore")
            desc = re.search(r'name="description" content="([^"]+)"', txt)
            print(f"=== {name} ({uid}) ===")
            if desc:
                print("Description:", desc.group(1))
            
            # Find colors and typography mentions
            colors = re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})', txt)
            hexes = list(set(["#" + c.lower() for c in colors]))[:15]
            print("Hexes:", hexes)
            
            # Check guidelines
            dos = re.findall(r'"children":"(Use[^"]+|Build[^"]+|Keep[^"]+)"', txt)
            donts = re.findall(r'"children":"(Don\'t[^"]+|Never[^"]+|Avoid[^"]+)"', txt)
            if dos:
                print("DO:", dos[:3])
            if donts:
                print("DONT:", donts[:3])
            print()
    except Exception as e:
        print(f"Error {name}: {e}")
