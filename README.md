# Site mirror using Python

This repository contains a minimal Python script to mirror a simple static site (HTML + images + CSS/JS) into a local `output/` folder.

Usage

1. Create a virtualenv (optional) and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the crawler (example):

```bash
python3 site_mirror.py https://samyo00.github.io/ --out output --max 200
```

Files
- `site_mirror.py`: crawler that downloads pages and assets and rewrites internal links for local browsing.
- `requirements.txt`: Python dependencies.

Site scaffold

- The `site/` folder contains a minimal static site scaffold you can customize: `index.html`, `publications/`, `projects/`, `programming/`, CSS in `site/assets/style.css`, and a placeholder avatar in `site/images/profile.svg`.

Deploy to GitHub Pages

1. Create a repo named `<your-github-username>.github.io` and push the `site/` contents to the repository root (not a subfolder), or push the `site/` folder to `gh-pages` branch and enable GitHub Pages from that branch.

Example (push `site/` to repo root):

```bash
cd site
git init
git remote add origin git@github.com:your-username/your-username.github.io.git
git add .
git commit -m "Initial personal site"
git push -u origin main
```

After pushing, GitHub Pages will serve `https://your-username.github.io/`.


Notes
- The script only downloads resources on the same host as the base URL.
- It is a lightweight scraper meant for small static sites; it doesn't execute JavaScript.
- Respect robots.txt and the site's terms before crawling. Add delays or rate-limiting if needed.
