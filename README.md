# Hosu

Hosu is a thumbnail generator for osu!.
Built in Python with a flexible architecture based on **Layout**, **Renderer**, **Variables** and **OsuAPI**.

---

## Requirements

- Python 3.11+
- Git (to work with the repository)
- pip

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/HegemonStudio/Hosu.git
cd Hosu

# 2. Create a virtual environment
python -m venv .venv/

# 3. Activate the environment
  # Linux
source .venv/bin/active
  # Windows (PowerShell)
.venv\Scripts\activate

# 4. Install required packages
pip install python-dotenv Pillow requests colorama rosu_pp_py
```

## Run

```bash
(.venv) python main.py
```

