# Cloudflare to PowerDNS Migration

This script migrates DNS records from Cloudflare to PowerDNS using the PowerDNS-Admin MySQL database. It fetches all DNS records from Cloudflare's API and adds them directly to your PowerDNS instance.

## Features

* Fetches DNS records from all zones in Cloudflare.
* Adds records to PowerDNS-Admin MySQL database.
* Supports common record types: `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`.
* Automatically creates entries in the `records` table of PowerDNS.
* Proxied Cloudflare records are not included in PowerDNS since PowerDNS doesn't support proxying.

## Prerequisites

* Python 3 installed on your machine.
* MySQL or MariaDB instance running for PowerDNS-Admin.
* Cloudflare API Token with `DNS:Edit` permissions.
* PowerDNS-Admin MySQL credentials.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MrAriaNet/cloudflare-to-pdns.git
cd cloudflare-to-pdns
```

### 2. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can manually install the required Python package:

```bash
pip install mysql-connector requests
```

### 3. Configure the script

Edit the script to set your Cloudflare API Token and PowerDNS MySQL credentials:

```python
# Cloudflare API settings
CLOUDFLARE_API_TOKEN = "YOUR_CF_API_TOKEN"
CF_API_URL = "https://api.cloudflare.com/client/v4/zones"

# MySQL (PowerDNS-Admin) settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "powerdns"
```

### 4. Run the script

After configuring the script, you can run it with:

```bash
python3 cf_to_pdns_mysql.py
```

### 5. Verify the migration

After running the script, check your PowerDNS-Admin instance to ensure the DNS records have been successfully added.

## How It Works

1. Fetches Cloudflare Zones: The script fetches all zones from Cloudflare using the Cloudflare API.
2. Fetches DNS Records: For each zone, the script fetches all DNS records associated with that zone.
3. Inserts Records into PowerDNS: The script then inserts the DNS records into your PowerDNS MySQL database, specifically into the `records` table.
4. Domain Mapping: It uses the domain names from Cloudflare to match records with corresponding domain entries in PowerDNS-Admin.

## Supported DNS Record Types

* `A`
* `AAAA`
* `CNAME`
* `MX`
* `TXT`
* `NS`
* `SRV`

## Notes

* Proxied Cloudflare Records: This script does not handle Cloudflare’s proxied records (orange cloud). Since PowerDNS doesn’t support proxying, these records will not be included in the migration.
* SRV Records: SRV records are included, but specific handling for CAA or PTR records is not implemented.

## Troubleshooting

If you encounter any issues, make sure:

* The `PowerDNS-Admin` MySQL instance is accessible and the correct credentials are provided.
* The `records` and `domains` tables exist in the PowerDNS-Admin MySQL database.
* The Cloudflare API token has the correct permissions (`DNS:Edit`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
