import mysql.connector
import requests

# Cloudflare API settings
CLOUDFLARE_API_TOKEN = "YOUR_CF_API_TOKEN"
CF_API_URL = "https://api.cloudflare.com/client/v4/zones"

# MySQL (PowerDNS-Admin) settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "powerdns"

# Cloudflare API headers
headers_cf = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
}

# MySQL connection function
def db_connect():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# --------------------------
#  Fetch all Cloudflare zones
# --------------------------
def get_cf_zones():
    zones = []
    page = 1
    while True:
        r = requests.get(CF_API_URL, headers=headers_cf, params={"page": page, "per_page": 50}).json()
        zones.extend(r["result"])
        if page >= r["result_info"]["total_pages"]:
            break
        page += 1
    return zones


# --------------------------
#  Fetch DNS records for a specific zone
# --------------------------
def get_cf_records(zone_id):
    url = f"{CF_API_URL}/{zone_id}/dns_records"
    records = []
    page = 1
    while True:
        r = requests.get(url, headers=headers_cf, params={"page": page, "per_page": 100}).json()
        records.extend(r["result"])
        if page >= r["result_info"]["total_pages"]:
            break
        page += 1
    return records


# --------------------------
#  Add DNS record to MySQL (PowerDNS-Admin)
# --------------------------
def add_record_to_db(zone_name, name, rtype, content, ttl):
    conn = db_connect()
    cursor = conn.cursor()
    
    # SQL query to insert the record into PowerDNS
    query = """
    INSERT INTO records (domain_id, name, type, content, ttl, priority)
    SELECT domain_id, %s, %s, %s, %s, 0
    FROM domains WHERE name = %s;
    """
    domain_name = zone_name.lower()
    cursor.execute(query, (name, rtype, content, ttl, domain_name))
    
    conn.commit()
    cursor.close()
    conn.close()


# --------------------------
#  Main migration process
# --------------------------
def migrate():
    print("Fetching Cloudflare zones...")
    zones = get_cf_zones()

    for z in zones:
        zone_name = z["name"]
        zone_id = z["id"]

        print(f"\n---- Zone: {zone_name} ----")

        # Get all DNS records from Cloudflare
        records = get_cf_records(zone_id)
        print(f"Found {len(records)} records in {zone_name}")

        # Add each record to MySQL (PowerDNS)
        for rec in records:
            name = rec["name"]
            rtype = rec["type"]
            content = rec["content"]
            ttl = rec["ttl"]

            # Skip specific records if necessary (for example: Proxied Cloudflare records, SRV, CAA)
            if rtype in ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV"]:
                add_record_to_db(zone_name, name, rtype, content, ttl)
                print(f"  + Added: {name} {rtype} {content}")

    print("\nMigration completed successfully!")


if __name__ == "__main__":
    migrate()
