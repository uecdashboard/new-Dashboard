"""
Streamlit Dashboard — Renders HTML content from a GitHub repository.

This app fetches HTML files stored in a GitHub repo and displays them
inside an interactive Streamlit dashboard. You can point it at any
public (or private, with a token) repo to pull in dashboard pages.
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import os

# ──────────────────────────────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GitHub HTML Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────
# Custom CSS for premium look
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Global ───────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ──────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* ── Header banner ────────────────────────────────────────────── */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, .35);
    }
    .dashboard-header h1 {
        color: #fff;
        margin: 0;
        font-weight: 700;
        font-size: 2rem;
    }
    .dashboard-header p {
        color: rgba(255,255,255,.85);
        margin: .4rem 0 0;
        font-size: 1rem;
    }

    /* ── Cards ────────────────────────────────────────────────────── */
    .metric-card {
        background: rgba(255,255,255,.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        transition: transform .2s, box-shadow .2s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(0,0,0,.18);
    }
    .metric-card h3 { margin: 0; font-size: 2rem; color: #667eea; }
    .metric-card p  { margin: .25rem 0 0; font-size: .9rem; color: #888; }

    /* ── Status badge ─────────────────────────────────────────────── */
    .status-ok  { color: #00c853; font-weight: 600; }
    .status-err { color: #ff1744; font-weight: 600; }

    /* ── Footer ───────────────────────────────────────────────────── */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: #666;
        font-size: .8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────
# Helper: fetch raw file from GitHub
# ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)  # cache for 5 minutes
def fetch_github_html(owner: str, repo: str, branch: str, path: str, token: str = "") -> str | None:
    """
    Fetch a raw file from GitHub.
    Uses the GitHub REST API so it works for both public and (with token) private repos.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        st.error(f"❌ Failed to fetch `{path}` — {e}")
        return None


def list_html_files(owner: str, repo: str, branch: str, folder: str, token: str = "") -> list[str]:
    """Return a list of .html file paths inside *folder* of the repo."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder}?ref={branch}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        items = resp.json()
        if isinstance(items, list):
            return [item["path"] for item in items if item["name"].endswith(".html")]
        return []
    except requests.RequestException:
        return []


# ──────────────────────────────────────────────────────────────────────
# Sidebar — repo settings
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Repository Settings")
    st.markdown("---")

    github_owner = st.text_input("GitHub Owner / Org", value="", placeholder="e.g. radwakamal")
    github_repo  = st.text_input("Repository Name", value="", placeholder="e.g. my-dashboard")
    github_branch = st.text_input("Branch", value="main")
    html_folder   = st.text_input("HTML Folder Path", value="dashboard", help="Folder inside the repo that contains your .html files")
    github_token  = st.text_input("GitHub Token (optional)", type="password", help="Required only for private repos")

    st.markdown("---")
    st.markdown("### 📄 Or paste HTML directly")
    manual_html = st.text_area("Paste HTML code", height=200, placeholder="<h1>Hello World</h1>")

    st.markdown("---")
    st.markdown(
        """
        ### 🚀 How it works
        1. Push `.html` files to your GitHub repo  
        2. Enter your repo details above  
        3. The dashboard fetches & renders them live  
        4. Files are **auto-refreshed** every 5 min  
        """
    )

# ──────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="dashboard-header">
        <h1>📊 GitHub HTML Dashboard</h1>
        <p>Live-render HTML pages stored in your GitHub repository</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────
# Main content
# ──────────────────────────────────────────────────────────────────────
tab_github, tab_manual, tab_guide = st.tabs(["🔗 GitHub HTML Files", "✏️ Manual HTML", "📖 Setup Guide"])

# ── Tab 1: GitHub files ──────────────────────────────────────────────
with tab_github:
    if github_owner and github_repo:
        with st.spinner("Fetching HTML file list from GitHub …"):
            html_files = list_html_files(github_owner, github_repo, github_branch, html_folder, github_token)

        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div class="metric-card"><h3>{len(html_files)}</h3><p>HTML files found</p></div>',
                unsafe_allow_html=True,
            )
        with col2:
            status_class = "status-ok" if html_files else "status-err"
            status_text  = "Connected" if html_files else "No files"
            st.markdown(
                f'<div class="metric-card"><h3 class="{status_class}">{status_text}</h3><p>Repo status</p></div>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<div class="metric-card"><h3>{github_branch}</h3><p>Active branch</p></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if html_files:
            selected_file = st.selectbox("Select an HTML file to render", html_files)

            if selected_file:
                with st.spinner(f"Loading `{selected_file}` …"):
                    html_content = fetch_github_html(
                        github_owner, github_repo, github_branch, selected_file, github_token
                    )

                if html_content:
                    st.success(f"✅ Loaded **{selected_file}** successfully")

                    # Render the HTML inside an iframe-like sandbox
                    components.html(html_content, height=700, scrolling=True)

                    # Expandable raw source
                    with st.expander("🔍 View raw HTML source"):
                        st.code(html_content, language="html")
        else:
            st.info(
                f"No `.html` files found in `{html_folder}/` on branch `{github_branch}`. "
                "Make sure you've pushed at least one HTML file to that folder."
            )
    else:
        st.warning("👈  Enter your **GitHub Owner** and **Repository Name** in the sidebar to get started.")

# ── Tab 2: Manual paste ──────────────────────────────────────────────
with tab_manual:
    st.markdown("### Paste & Preview HTML")
    if manual_html.strip():
        components.html(manual_html, height=600, scrolling=True)
    else:
        st.info("Paste some HTML in the sidebar text area to preview it here.")

# ── Tab 3: Setup guide ──────────────────────────────────────────────
with tab_guide:
    st.markdown(
        """
        ## 🛠️ Full Setup Guide

        ### Step 1 — Install Streamlit locally
        ```bash
        pip install streamlit
        ```

        ### Step 2 — Create your GitHub repository
        1. Go to [github.com/new](https://github.com/new) and create a new repo (e.g. `my-dashboard`).
        2. Inside the repo, create a folder called **`dashboard/`**.
        3. Add your `.html` files there.

        **Example repo structure:**
        ```
        my-dashboard/
        ├── app.py              ← this Streamlit file
        ├── requirements.txt
        └── dashboard/
            ├── sales_report.html
            ├── analytics.html
            └── overview.html
        ```

        ### Step 3 — Run locally
        ```bash
        streamlit run app.py
        ```

        ### Step 4 — Deploy on Streamlit Community Cloud 🚀
        1. Push your code (including `app.py` and `requirements.txt`) to GitHub.
        2. Go to **[share.streamlit.io](https://share.streamlit.io/)**.
        3. Sign in with GitHub.
        4. Click **"New app"** → select your repo, branch, and `app.py`.
        5. Hit **Deploy** — you'll get a live URL like `https://your-app.streamlit.app`.

        ### Step 5 — Add secrets (for private repos)
        In Streamlit Cloud → App Settings → Secrets, add:
        ```toml
        GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"
        ```
        Then read it in code with `st.secrets["GITHUB_TOKEN"]`.

        ---
        > **Tip:** Every time you push new HTML to your GitHub repo,
        > the dashboard will pick it up automatically (within ~5 min cache window).
        """
    )

# ──────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">Built with ❤️ using Streamlit · Connected to GitHub</div>',
    unsafe_allow_html=True,
)
