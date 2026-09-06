import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from io import BytesIO
import time

st.set_page_config(page_title="Website URL Crawler", page_icon="🔗")
st.title("🔗 Website URL Crawler")
st.write(
    "Crawlt een website (binnen hetzelfde domein), verzamelt alle gevonden URL's "
    "en genereert een Excel-overzicht met de URL opgesplitst per niveau."
)

start_url = st.text_input("Start URL", placeholder="https://www.voorbeeld.nl")
col1, col2 = st.columns(2)
with col1:
    max_pages = st.number_input("Max. aantal pagina's", min_value=1, max_value=5000, value=200, step=50)
with col2:
    delay = st.number_input("Vertraging tussen requests (sec)", min_value=0.0, max_value=5.0, value=0.3, step=0.1)

skip_extensions = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".zip", ".doc", ".docx",
                    ".xls", ".xlsx", ".mp4", ".mp3", ".svg", ".css", ".js")


def crawl(start_url, max_pages, delay, progress_callback=None):
    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = [start_url]
    found_urls = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200 or "text/html" not in resp.headers.get("Content-Type", ""):
                continue
            found_urls.append(url)

            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"]).split("#")[0].rstrip("?")
                parsed = urlparse(link)
                if parsed.netloc != domain:
                    continue
                if link.lower().endswith(skip_extensions):
                    continue
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
        except Exception:
            continue

        if progress_callback:
            progress_callback(len(visited), len(found_urls))
        time.sleep(delay)

    return found_urls


def urls_to_dataframe(urls):
    parsed_rows = []
    max_levels = 0

    for url in urls:
        parsed = urlparse(url)
        hoofddomein = f"{parsed.scheme}://{parsed.netloc}"
        path_parts = [p for p in parsed.path.split("/") if p]

        levels = []
        cumulative = ""
        for part in path_parts:
            cumulative += f"/{part}"
            levels.append(cumulative + "/")

        max_levels = max(max_levels, len(levels))
        parsed_rows.append((url, hoofddomein, levels))

    columns = ["Volledige URL", "Hoofddomein"] + [f"Niveau {i+1}" for i in range(max_levels)]
    rows = []
    for url, hoofddomein, levels in parsed_rows:
        row = [url, hoofddomein] + levels + [""] * (max_levels - len(levels))
        rows.append(row)

    return pd.DataFrame(rows, columns=columns)


if st.button("Start crawl", type="primary", disabled=not start_url):
    status = st.empty()
    progress_bar = st.progress(0)

    def update_progress(visited_count, found_count):
        pct = min(visited_count / max_pages, 1.0)
        progress_bar.progress(pct)
        status.text(f"Bezocht: {visited_count} | Gevonden pagina's: {found_count}")

    with st.spinner("Bezig met crawlen..."):
        urls = crawl(start_url, max_pages, delay, update_progress)

    if not urls:
        st.error("Geen pagina's gevonden. Controleer de URL of probeer het opnieuw.")
    else:
        df = urls_to_dataframe(urls)
        st.success(f"✅ {len(urls)} pagina's gevonden")
        st.dataframe(df, use_container_width=True)

        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        st.download_button(
            "📥 Download Excel-overzicht",
            data=buffer.getvalue(),
            file_name="url_overzicht.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
