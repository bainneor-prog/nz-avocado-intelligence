# NZ Avocado Intelligence — API starter

Development-only Streamlit starter to test FAOSTAT, USDA FAS, UN Comtrade preview, and FRED connections.

## Local setup (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
notepad .streamlit\secrets.toml
streamlit run app.py
```

Fill in actual keys in `.streamlit/secrets.toml`. **Never commit that file.** If you've already created a local secrets file, keep it and don't overwrite it with the example.

## Streamlit Community Cloud

Deploy `app.py` from GitHub. Set the same four secrets in the app's **Secrets** settings. Do not publish this testing app publicly: it can trigger authenticated API requests.

## Notes

- Comtrade test uses the **preview** endpoint, not the full historical endpoint.
- USDA test targets **2016** because that year has been verified for NZ.
- FRED test uses `DEXUSNZ` (USD per NZD exchange rate series); the API may return missing observations for non-business days.
- This starter is for testing, not a production ingestion pipeline.
- Check source licences and usage conditions before publishing datasets.
