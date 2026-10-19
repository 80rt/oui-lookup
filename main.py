import sqlite3
import argparse
import subprocess

db_path = "vendor.db"


def arpDump(oui):      
    arp = subprocess.run(
    ["ip", "-4", "neigh"],
    capture_output=True,
    text=True,
    check=True,
)

    for line in arp.stdout.splitlines():
        parts = line.split()
        if "lladdr" in parts:
            mac = parts[parts.index("lladdr") + 1] 
    oui = mac.replace(":", "").replace("-", "")[:6].upper()

    with sqlite3.connect(db_path) as db:
        cursor = db.execute(
            'SELECT "Organization Name" FROM oui WHERE Assignment = ?',
            (oui,),
        )
        row = cursor.fetchone()

        manufacturer = row[0] if row else "Manufacturer not found"
        print(mac, oui, manufacturer)

parser = argparse.ArgumentParser()
parser.add_argument("oui", help="OUI to look up")
args = parser.parse_args()

arpDump(args.oui)
