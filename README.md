# DataDashboardPython
## Environment setup
Make sure that you have Python installed. Then, create virtual environment:

```
python3 -m venv .venv
```

Activate .venv:
* on Windows
```
.venv\Scripts\Activate.ps1
```
* on Linux/macOS
```
source .venv/bin/activate
```
Download necessary dependencies.
```
pip install streamlit dash yfinance dash_bootstrap_components scikit-learn scikit-learn-extra
```

Now we are ready to build our first dashboard apps :)

## Environment setup (Using venv)
Make sure that you have Python installed. We need to create the  virtual enviroment inside BOTH the dash and streamlit folders:

First, navigate to the folder:
```
cd .\streamlit\
OR
cd .\dash\
```

then create the virtual enviroment inside a .venv folder:
```
python -m venv .venv
```

The virtual environment can then be enabled using:
* on Windows
```
.venv\Scripts\Activate.ps1
```

* on Linux/macOS
```
source .venv/bin/activate
```

After the virtual enviroment is enabled the requirements can be installed using:
```
python -m pip install -r .\requirements.txt
```

## Environment setup (Using docker)
Make sure that Docker is installed and that the Docker Engine is running (Starting the Docker Desktop should do the trick)

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
### Project Structure
Here is the file structure of a multi-page streamlit project.

```
├── streamlit_app.py
├── pages
    ├── graph.py
    ├── home.py
    └── todolist.py
```