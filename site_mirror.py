import os
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

BASE_DELAY = 0.3


def make_dirs_for_path(path):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def save_binary(url, out_path):
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
    except Exception:
        return False
    make_dirs_for_path(out_path)
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
    return True


def save_html(text, out_path):
    make_dirs_for_path(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)


def is_same_site(url, base_netloc):
    try:
        p = urlparse(url)
        return (p.netloc == "" or p.netloc == base_netloc)
    except Exception:
        return False


def normalize_link(href, base_url):
    if not href:
        return None
    href = href.split('#')[0]
    return urljoin(base_url, href)


def local_path_for_url(url, base_url, out_dir):
    p = urlparse(url)
    base = urlparse(base_url)
    rel = p.path
    if rel.endswith('/') or rel == '':
        rel = rel + 'index.html'
    if rel.startswith('/'):
        rel = rel[1:]
    out_path = os.path.join(out_dir, rel)
    return out_path


def crawl(base_url, out_dir='output', max_pages=200):
    session = requests.Session()
    parsed_base = urlparse(base_url)
    base_netloc = parsed_base.netloc

    to_visit = [base_url]
    visited = set()

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        print('Fetching', url)
        try:
            r = session.get(url, timeout=15)
            r.raise_for_status()
            html = r.text
        except Exception as e:
            print('  failed:', e)
            visited.add(url)
            time.sleep(BASE_DELAY)
            continue

        soup = BeautifulSoup(html, 'html.parser')

        # Download images
        for img in soup.find_all('img'):
            src = img.get('src')
            full = normalize_link(src, url)
            if not full:
                continue
            if not is_same_site(full, base_netloc):
                continue
            local = local_path_for_url(full, base_url, out_dir)
            if save_binary(full, local):
                img['src'] = os.path.relpath(local, os.path.dirname(local_path_for_url(url, base_url, out_dir)))

        # Download css and js
        for tag, attr in (('link', 'href'), ('script', 'src')):
            for t in soup.find_all(tag):
                href = t.get(attr)
                if not href:
                    continue
                full = normalize_link(href, url)
                if not is_same_site(full, base_netloc):
                    continue
                local = local_path_for_url(full, base_url, out_dir)
                if save_binary(full, local):
                    t[attr] = os.path.relpath(local, os.path.dirname(local_path_for_url(url, base_url, out_dir)))

        # Rewrite internal links and queue pages
        for a in soup.find_all('a'):
            href = a.get('href')
            full = normalize_link(href, url)
            if not full:
                continue
            if not is_same_site(full, base_netloc):
                continue
            # make relative link
            local = local_path_for_url(full, base_url, out_dir)
            a['href'] = os.path.relpath(local, os.path.dirname(local_path_for_url(url, base_url, out_dir)))
            if full not in visited and full not in to_visit:
                to_visit.append(full)

        out_path = local_path_for_url(url, base_url, out_dir)
        save_html(str(soup), out_path)
        visited.add(url)
        time.sleep(BASE_DELAY)

    print('Crawled', len(visited), 'pages. Output in', out_dir)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('base', nargs='?', default='https://samyo00.github.io/')
    p.add_argument('--out', default='output')
    p.add_argument('--max', type=int, default=200)
    args = p.parse_args()
    crawl(args.base, args.out, args.max)
