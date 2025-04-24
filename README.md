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

First, navigate to the folder:
```
cd .\streamlit\
OR
cd .\dash\
```

### Dash

### Streamlit
Create the docker container by using the command:
```
docker compose up
```

The app should be running now, in case that the app doesn't load try changing the url to localhost:8501

## Dash
### Project Structure
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
Streamlit is an open-source Python framework used to build interactive data apps - in only a few lines of code. It allows us to focus on what's important to us, instead of worrying about the code.

### Key features

- **Intuitive Syntax**
    One of Streamlit’s standout features is that it has intuitive default styles “baked in” so you can deploy and share polished apps with anyone anywhere. For example, to write a header, you use st.header(). To add some text, you use st.write(). Need a divider? Just use st.divider().
    No CSS, HTML, or JavaScript experience required!

- **Seamlessly Composable**
    With Streamlit, you don’t have to do any “app thinking” – you don’t have to think about the UI, the styling, or the routing. It simply extends what you’re already doing in Python. 

- **Your go-to UI**
    Streamlit gets you to a working version 0 of your app faster. You can get your app in front of users faster, get feedback faster, and improve faster. Streamlit makes your iteration cycles shorter.

### Project Structure
Here is the file structure of a multi-page streamlit project.

```
├── streamlit_app.py
├── pages
    ├── graph.py
    ├── home.py
    └── todolist.py
```