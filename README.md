# 📊 GitHub HTML Dashboard (Streamlit)

A **Streamlit** dashboard that fetches and renders `.html` files from a
**GitHub** repository — perfect for sharing reports, data visualisations,
or any static HTML content through an interactive web UI.

## ✨ Features

| Feature | Description |
|---------|------------|
| **Live GitHub sync** | Automatically lists & renders HTML files from any GitHub repo |
| **Private repo support** | Use a Personal Access Token (PAT) for private repositories |
| **Manual HTML preview** | Paste raw HTML directly for quick previews |
| **Auto-refresh** | Content re-fetched every 5 minutes (configurable) |
| **One-click deploy** | Push to GitHub → deploy on Streamlit Community Cloud |

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/<YOUR_USERNAME>/streamlit-dashboard.git
cd streamlit-dashboard
pip install -r requirements.txt
```

### 2. Run locally

```bash
streamlit run app.py
```

### 3. Add your HTML files

Place `.html` files inside the **`dashboard/`** folder (or change the folder
name in the sidebar settings).

### 4. Deploy to Streamlit Cloud

1. Push to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app** → select repo → select `app.py` → **Deploy**.

## 📁 Project Structure

```
streamlit-dashboard/
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── .gitignore
├── README.md
└── dashboard/           # Your HTML files live here
    └── sample.html      # Example dashboard page
```

## 🔒 Private Repos

For private repos, create a GitHub **Personal Access Token** and either:
- Paste it in the sidebar token field (local use), **or**
- Add it as a Streamlit Cloud secret:
  ```toml
  # .streamlit/secrets.toml  (local)  OR  Streamlit Cloud → Secrets
  GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"
  ```

## 📄 License

MIT — free to use and modify.
