import glob
import markdown
from itertools import groupby
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

# Configuration
SITE_TITLE = "Lucian Marin"
IMG_ROOT = "https://lucianmarin.github.io/"

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

def get_all_posts():
    # Find all .md files in _posts and subdirectories
    # Note: glob order is OS dependent, so we must sort manually.
    files = glob.glob('_posts/**/*.md', recursive=True)

    # Sort files by path descending (replicating PHP krsort)
    # paths like _posts/2020/... come before _posts/2009/...
    files.sort(reverse=True)

    posts = []
    for filepath in files:
        post = parse_file(filepath)
        posts.append(post)

    return posts

def parse_file(filepath):
    post = {}
    body_lines = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_frontmatter = False
        delimiter_count = 0

        # PHP logic simulation
        # It seems to assume frontmatter exists.

        for line in lines:
            if delimiter_count != 2:
                if line.strip() == "---":
                    delimiter_count += 1
                    in_frontmatter = True
                else:
                    if ":" in line:
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            val = parts[1].strip().strip('"')
                            post[key] = val
            else:
                body_lines.append(line)

        body = "".join(body_lines)

        # Replacements
        # str_replace("(/images/", "(".$GLOBALS['img_root']."images/", $body);
        body = body.replace("(/images/", f"({IMG_ROOT}images/")

        # Parse Markdown
        # Enabling extra extensions to match typical PHP Parsedown behavior if needed,
        # but standard markdown is usually enough. 'fenced_code' is common.
        html_body = markdown.markdown(body, extensions=['fenced_code', 'tables'])
        post['body'] = html_body

        filename = Path(filepath).stem
        parts = filename.split('-')
        if len(parts) >= 4:
            post['year'] = parts[0]
            post['month'] = parts[1]
            post['day'] = parts[2]
            post['name'] = parts[3]

        # Ensure title and date exist
        if 'title' not in post:
            post['title'] = "Untitled"
        if 'date' not in post:
            # If frontmatter didn't have date, use extracted parts or empty
            if 'year' in post and 'month' in post and 'day' in post:
                post['date'] = f"{post['year']}-{post['month']}-{post['day']}"
            else:
                post['date'] = ""

        return post
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return {"title": "Error", "date": "", "body": "Could not parse post.", "id": -1}

# Cache posts in memory on startup (or we could load per request)
# For a simple blog, loading per request is fine for dev, but let's cache.
# However, for 'hot reload' during dev, loading per request is better.
# I'll load per request for simplicity and robustness against file changes.
# Optimization can be added later.

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    posts = get_all_posts()
    grouped_posts = []

    for year, items in groupby(posts, key=lambda x: x.get('year', 'Unknown')):
        grouped_posts.append((year, list(items)))

    return templates.TemplateResponse("index.html", {
        "request": request,
        "grouped_posts": grouped_posts,
        "site_title": SITE_TITLE,
        "title": SITE_TITLE,
        "date": "today" # PHP used "today" string
    })

@app.get("/{year}/{month}/{day}/{name}", response_class=HTMLResponse)
async def read_post(request: Request, year: str, month: str, day: str, name: str):
    filepath = f"_posts/{year}/{year}-{month}-{day}-{name}.md"

    if not Path(filepath).is_file():
        raise HTTPException(status_code=404, detail="Post not found")

    post = parse_file(filepath)

    return templates.TemplateResponse("post.html", {
        "request": request,
        "post": post,
        "site_title": SITE_TITLE,
        "title": post['title'],
        "date": post.get('date', '')
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
