# DataDashboardPython
## Environment setup
Make sure that you have Python installed. Then, create virtual environment:

```
python3 -m venv .venv
```

Activate .venv:
* on Windows
```
.venv\Scripts\activate
```
* on Linux/macOS
```
source .venv/bin/activate
```
Download necessary dependencies.
```
pip install streamlit dash yfinance
```

Now we are ready to build our first dashboard apps :)

## Dash
Here is the file structure of a multi-page dash project.

```
├── app.py
├── assets
│   └── 01_style.css
└── pages
    ├── archive.py
    ├── exchange-rate.py
    ├── home.py
```

## Streamlit