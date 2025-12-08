# 📘 News Digest – Automated Daily Markdown News Summaries

News Digest is a lightweight automated pipeline that:

- Fetches headlines from selected Korean and English RSS news sources
- Saves a daily digest as a Markdown file into:

```
digests/en/YYYY/YYYY-MM-DD.md
digests/ko/YYYY/YYYY-MM-DD.md
```


The project is structured to be **simple, extensible**, and fully automated using **GitHub Actions**.

---

## 🌐 Supported Sources

You can add or remove any RSS feed inside `src/config.yml`.

Typical sources include:

- **Korean**: Hankyung, Maeil Business, Seoul Economic Daily  
- **English**: Financial Times, The Economist, WSJ

💡 Currently the project supports separate output folders for Korean (`ko/`) and English (`en/`).

---

## 📁 Project Structure

```
danews_daily/
├─ digests/
│ ├─ en/2025/
│ ├─ ko/2025/
├─ src/
│ └─ news_digest.py
│ └─ config.yml
├─ .github/
│ └─ workflows/
│ └─ daily.yml
├─ README.md
└─ requirements.txt
```

- **digests/** → auto-generated Markdown summaries  
- **src/news_digest.py** → main script (fetch → export)  
- **GitHub Actions workflow** → runs daily and commits new output  

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/news-digest.git
cd news-digest
```


2. Install dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run manually
```
python src/news_digest.py
```

Daily markdown output will appear under:

```
digests/YYYY/YYYY-MM-DD.md
```

---

## 🤖 Automation via GitHub Actions

This project includes a workflow (`.github/workflows/daily.yml`) that:

- Runs every day at a specified UTC time
- Fetches headlines
- Generates a Markdown digest
- Commits and pushes the new digest back to the repository automatically

To manually trigger the job:

1. Go to GitHub → Actions
2. Select Daily News Digest
3. Click Run workflow

---

