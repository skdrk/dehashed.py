# dehashed.py

A Python CLI tool to query the [DeHashed](https://dehashed.com) v2 API. Search breach databases for emails, passwords, hashes, usernames, IPs and more.

## Requirements

```bash
pip install requests colorama
```

## Configuration

Edit the top of `dehashed.py` and set your API key:

```python
API_KEY = 'your_api_key_here'
```

You can find your API key in your DeHashed account under **API Documentation**.

> **Note:** DeHashed migrated to API v2 in 2025. This script uses the new `/v2/search` endpoint with header-based authentication. The old HTTP Basic Auth method no longer works.

---

## Usage

```bash
python dehashed.py [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-q`, `--query` | Search query (e.g. `domain:example.com`) |
| `-l`, `--list` | Path to a file with one query per line |
| `-f`, `--fields` | Comma-separated fields to display per line |
| `-p`, `--pretty` | Pretty print all fields for each entry |
| `-o`, `--out_file` | Save output to a file |
| `-d`, `--dedupe` | Remove duplicate results |
| `--page` | Page number (default: 1) |
| `--size` | Results per page, max 10000 (default: 100) |
| `-v`, `--verbose` | Verbose mode |

---

## Query Syntax

DeHashed supports field-based queries:

| Field | Example |
|-------|---------|
| `email` | `email:bob@example.com` |
| `domain` | `domain:example.com` |
| `username` | `username:johndoe` |
| `password` | `password:hunter2` |
| `name` | `name:"John Doe"` |
| `phone` | `phone:+34600000000` |
| `ip_address` | `ip_address:192.168.1.1` |

---

## Examples

**Raw JSON output:**
```bash
python dehashed.py -q "domain:example.com"
```

**Pretty print, field by field:**
```bash
python dehashed.py -q "domain:example.com" -p
```

**Show only email, password and hash, one per line:**
```bash
python dehashed.py -q "domain:example.com" -f email,password,hashed_password
```

**Save filtered results to a file:**
```bash
python dehashed.py -q "domain:example.com" -f email,password,hashed_password -o results.txt
```

**Remove duplicates:**
```bash
python dehashed.py -q "domain:example.com" -f email,username -d
```

**Run multiple queries from a file:**
```bash
python dehashed.py -l queries.txt -f email,password -o results.txt
```

**Paginate through results:**
```bash
python dehashed.py -q "domain:example.com" --size 500 --page 2
```

---

## Available Fields for `-f`

```
email, password, hashed_password, username, name,
phone, address, ip_address, database_name
```

---

## Output Format

When using `-f`, each result is printed as a pipe-separated line:

```
paco@example.com | hunter2 | 
pepe@example.com |  | 5f4dcc3b5aa765d61d8327deb882cf99
```

---

## Notes

- Each search costs **1 credit** from your DeHashed balance.
- Max pagination depth is **50,000 results** per query (`page * size ≤ 50,000`).
- Deep pagination (beyond 10,000 results) requires sequential page fetching within a 10-minute session window.

---

## Disclaimer

This tool is intended for **authorized security research, penetration testing, and OSINT investigations** only. Usage must comply with [DeHashed's Terms of Service](https://dehashed.com/terms) and applicable laws. The author is not responsible for any misuse.
