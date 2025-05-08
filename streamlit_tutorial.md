# Streamlit
* Open-source Python library, released in 2019, for building interactive web apps
* Designed for data scientists and machine learning engineers
* Enables rapid prototyping with minimal code
* [Documentation](https://docs.streamlit.io/)

## Installation and environment setup

### Venv
For Windows:
```
python -m venv .venv
.venv\Scripts\Activate
```

For Linux/MacOS:
```
python -m venv .venv
source .venv/bin/activate
```

Install required libraries (specified in requirements.txt):
```
pip install -r requirements.txt
```

Launch the project using:
```
streamlit run streamlit_app.py
```
OR
```
python -m streamlit run streamlit_app.py
```

### Docker
Make sure that Docker is installed and that the Docker Engine is running (Starting the Docker Desktop should do the trick)

Then while in the streamlit folder
```
docker compose up
```

## Project structure

```
├── streamlit_app.py
├── pages
    ├── graph.py
    ├── home.py
    ├── meteorites.py
    ├── streamlit-reference.py
    ├── todolist.py
```

***
---
## Functionality
- Graph page:
    1. Select stock instrument
    2. View price history over a selected period of time 
- Meteorites page:
    1. Select map modes
    2. View meteorite impact map
- Streamlit reference:
    1. Quick guide to streamlit syntax and functionality
- Todo List:
    1. Add tasks to list
    2. Remove tasks from list
    3. Sort the tasks by date of creation
    4. Save the tasks to a .json file (automatic)
---

# Streamlit multi-page app
## 1. App Layout

### 1.1. `streamlit_app.py`
This will be the main application file for the streamlit project. Create a file called **streamlit_app.py** in your **streamlit** folder:
```python
import streamlit as st

# In this section the pages for the app are added. Leave it empty for now and add pages as you go.
pages = [
    st.Page("<relative_path_to_file>", title="Example page", icon=":material/token:")
]

pg = st.navigation(pages, position="sidebar", expanded=True)

pg.run()
```

### 1.2. `graph.py`
#### 1.2.1. Imports
```python
import streamlit as st 
import yfinance as yf # Yahoo Finance is used for getting the stock data
import plotly.graph_objects as go # Plotly is used for plotting the data
```

#### 1.2.2. Getting the stock data

```python
def get_stock_data(symbol, period="1y", interval="1d"):
    """Fetch stock data from Yahoo Finance."""
    try:
        stock_data = yf.Ticker(symbol)
        stock_history = stock_data.history(period = period, interval = interval)
        if stock_history.empty:
            st.warning(f"No data available for {symbol} with period '{period}' and interval '{interval}'.")
            return None

        return stock_history
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None
```

#### 1.2.3. Search button and plot creation
Create any necessary (or unnecessary) text and headers, add buttons which utilize the created functions. Use plotly to create the plot (or plots).
```python
st.write("## Search for a stock symbol")
stock_symbol = st.text_input("Enter stock symbol (e.g., AAPL, MSFT):", "AAPL", help="Start typing to see suggestions.")
suggested_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NFLX", "NVDA", "BABA", "INTC"]
if stock_symbol not in suggested_symbols:
    st.warning("Suggested symbols: " + ", ".join(suggested_symbols))
time_period = st.selectbox("Select time period:", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])
interval = st.selectbox("Select interval:", ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1mo"])

if st.button("Search"):
    stock_data = get_stock_data(stock_symbol, time_period, interval)
    if stock_data is not None:
        st.divider()
        st.write(f"### You selected: {stock_symbol}")
        st.write("## Historical Data")
        st.dataframe(stock_data)

        try:
            st.divider()
            st.write("## Stock Price Candle Graph")
            fig = go.Figure(data=[go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close']
            )])
            fig.update_layout(title=f"Candlestick Chart for {stock_symbol}", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error plotting data: {e}")
    else:
        st.write("No data available")
```

#### 1.2.4. Adding the page to navigation
Add the page in the `pages` section of `app.py`.
```python
pages = [
    st.Page("pages/graph.py", title="Graphs", icon=":material/monitoring:")
]
```

### 1.3. `todolist.py`
#### 1.3.1. Imports
```python
import streamlit as st
import json # For saving the tasks in a json format and reading it from file
import os # For loading the locally saved tasks
```

#### 1.3.2. Functions
```python
# File to store notes
NOTES_FILE = "notes.json"

# Function to load notes from file
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save notes to file
def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file)

# Function to remove notes
def remove_note(index):
    """Remove a note by index."""
    if 0 <= index < len(st.session_state["notes"]):
        st.session_state["notes"].pop(index)
        save_notes(st.session_state["notes"])
```

#### 1.3.3. Buttons and page layout
```python
# Initialize session state for notes
if "notes" not in st.session_state:
    st.session_state["notes"] = load_notes()

st.title("To-Do List")

# Input for new note
new_title = st.text_input("Note Title:")
new_note = st.text_area("Note Content:")

# Button to add the note
if st.button("Add Note"):
    if new_title.strip() and new_note.strip():  # Ensure title and content are not empty
        st.session_state["notes"].append({"title": new_title.strip(), "content": new_note.strip()})
        save_notes(st.session_state["notes"])  # Save notes to file
        st.success("Note added!")
    else:
        st.warning("Please enter both a title and content for the note.")

# Sorting options
sort_order = st.radio("Sort Notes By:", ("Oldest to Newest", "Newest to Oldest"))

# Display the list of notes
if st.session_state["notes"]:
    st.divider()
    st.subheader("Your Notes:")
    notes = st.session_state["notes"]
    if sort_order == "Newest to Oldest":
        notes = reversed(notes)
    for i, note in enumerate(notes, start=1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{i}. {note['title']}**")
            st.write(note["content"])
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                remove_note(i - 1)
                st.rerun()
else:
    st.info("No notes yet. Add your first note!")
```