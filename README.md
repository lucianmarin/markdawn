# Markdawn (formerly Pressdown PHP)

A lightweight, flat-file blog engine converted from PHP to Python using FastAPI. Markdawn is designed to be simple, fast, and compatible with Jekyll-style Markdown posts.

## Features

- **Flat-file based**: No database required. All posts are stored as Markdown files.
- **Jekyll compatibility**: Supports Jekyll-style YAML front matter for post metadata (title, date, etc.).
- **Python Powered**: Built with FastAPI and Python-Markdown.
- **Dynamic Routing**: Automatically lists and serves posts based on the directory structure.
- **Minimalistic Layout**: Clean and simple HTML5 templates using Jinja2.

## Project Structure

- `_posts/`: Contains your blog posts in Markdown format.
- `templates/`: Jinja2 templates (`layout.html`, `index.html`, `post.html`).
- `static/`: CSS, SASS, fonts, and images.
- `main.py`: The FastAPI application entry point.

## Getting Started

### Prerequisites

- Python 3.7 or higher.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lucianmarin/markdawn.git
   cd markdawn
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open your browser and navigate to `http://localhost:8000`.

## Configuration

Site-wide settings can be found in `main.py`:

```python
AUTHOR = "Lucian Marin"
DESCRIPTION = "Bio"
```

## Creating Posts

Add a new Markdown file to the `_posts/` directory (e.g., `_posts/2026/hello.md`). Each file should start with YAML front matter:

```markdown
---
title: "My New Post"
date: "2026-01-09"
---

Your content goes here...
```
