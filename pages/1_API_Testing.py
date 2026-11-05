"""Development-only API smoke tests. Do not expose publicly."""
import time
import requests
import streamlit as st

st.title("API connection tests")
st.warning("Development-only page. Restrict access before deploying publicly.")

TESTS = {
    "FAOSTAT — NZ avocado production (2024)": {
        "url": "https://faostatservices.fao.org/api/v1/en/data/QCL",
        "params": {"area": "156", "item": "572", "year": "2024"},
        "secret": "FAOSTAT_KEY", "header": "Authorization", "prefix": "Bearer ",
        "kind": "faostat",
    },
    "USDA FAS — NZ avocado exports (2016)": {
        "url": "https://api.fas.usda.gov/api/gats/UNTradeExports/reporterCode/NZ/year/2016",
        "secret": "USDA_KEY", "header": "X-Api-Key", "prefix": "", "kind": "usda",
    },
    "UN Comtrade — NZ avocado exports (2024 preview)": {
        "url": "https://comtradeapi.un.org/public/v1/preview/C/A/HS",
        "params": {"period": "2024", "reporterCode": "554", "cmdCode": "080440", "flowCode": "X"},
        "secret": "COMTRADE_KEY", "header": "Ocp-Apim-Subscription-Key", "prefix": "", "kind": "comtrade",
    },
    "FRED — NZ economic series (test)": {
        "url": "https://api.stlouisfed.org/fred/series/observations",
        "params": {"series_id": "DEXUSNZ", "file_type": "json", "limit": "5", "sort_order": "desc"},
        "secret": "FRED_KEY", "kind": "fred",
    },
}

choice = st.selectbox("Choose source", list(TESTS))
config = TESTS[choice]

if st.button("Run test", type="primary"):
    secret_name = config["secret"]
    secret = st.secrets.get(secret_name)
    if not secret:
        st.error(f"Missing {secret_name} in Streamlit Secrets.")
        st.stop()
    params = dict(config.get("params", {}))
    headers = {}
    if config["kind"] == "fred":
        params["api_key"] = secret
    else:
        headers[config["header"]] = config.get("prefix", "") + secret
    try:
        start = time.perf_counter()
        response = requests.get(config["url"], params=params, headers=headers, timeout=30)
        elapsed = time.perf_counter() - start
        st.metric("HTTP status", response.status_code)
        st.metric("Response time", f"{elapsed:.2f} s")
        response.raise_for_status()
        payload = response.json()
        kind = config["kind"]
        if kind == "faostat":
            records = payload.get("data", [])
        elif kind == "usda":
            records = [r for r in payload if r.get("hS6Code") == "080440"]
        elif kind == "comtrade":
            records = payload.get("data", [])
        else:
            records = payload.get("observations", [])
        st.metric("Matching records", len(records))
        if records:
            st.dataframe(records[:20], use_container_width=True)
        else:
            st.warning("Request succeeded but no matching records were found.")
        if kind == "comtrade":
            st.info("This endpoint is PREVIEW data, not validated full historical coverage.")
    except requests.HTTPError:
        st.error(f"API returned HTTP {response.status_code}. Verify permissions, parameters, and provider status.")
    except requests.RequestException as exc:
        st.error(f"Network request failed: {type(exc).__name__}. Check connectivity and server logs.")
    except (ValueError, TypeError, AttributeError):
        st.error("Response format was not the expected JSON structure.")
