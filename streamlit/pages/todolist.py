import streamlit as st

# Initialize session state for notes
if "notes" not in st.session_state:
    st.session_state["notes"] = []

st.title("To-Do List")

# Input for new note
new_title = st.text_input("Note Title:")
new_note = st.text_area("Note Content:")

# Button to add the note
if st.button("Add Note"):
    if new_title.strip() and new_note.strip():  # Ensure title and content are not empty
        st.session_state["notes"].append({"title": new_title.strip(), "content": new_note.strip()})
        st.success("Note added!")
    else:
        st.warning("Please enter both a title and content for the note.")

# Sorting options
sort_order = st.radio("Sort Notes By:", ("Oldest to Newest", "Newest to Oldest"))

# Display the list of notes
if st.session_state["notes"]:
    st.subheader("Your Notes:")
    notes = st.session_state["notes"]
    if sort_order == "Newest to Oldest":
        notes = reversed(notes)
    for i, note in enumerate(notes, start=1):
        st.write(f"**{i}. {note['title']}**")
        st.write(note["content"])
else:
    st.info("No notes yet. Add your first note!")