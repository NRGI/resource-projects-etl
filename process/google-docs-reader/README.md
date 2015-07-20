# Transform from Google Docs

This script will read a **published** google docs spreadsheet, configured according to a standard template, and will parse out selected sheets.

It caches entities as it reads across sheets, so if a company is discovered across multiple sheets (for example) it will assign the same identifier each time. 

## Usage

```
python transform-from-gdocs.py <SPREADSHEET URL>
```

