import streamlit as st
import json
import os

# Configuration
DB_FILE = "notes_db.json"
CATEGORIES = ["University", "Personal", "Projects"]

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize session state for data
if "notes" not in st.session_state:
    st.session_state.notes = load_data()

# --- UI Layout ---
st.title("📝 My Local Notebook")
st.write("Write down your thoughts and organize them by category.")

# Sidebar for adding new notes
with st.sidebar:
    st.header("Add New Note")
    new_title = st.text_input("Title")
    
    # New Category Selection
    new_category = st.selectbox("Category", options=CATEGORIES)
    
    new_content = st.text_area("Content")
    
    if st.button("Save Note"):
        if new_title and new_content:
            new_note = {
                "id": len(st.session_state.notes),
                "title": new_title,
                "category": new_category,
                "content": new_content
            }
            st.session_state.notes.append(new_note)
            save_data(st.session_state.notes)
            st.success(f"Saved to {new_category}!")
            st.rerun()
        else:
            st.error("Please provide both a title and content.")

# --- Search & Filter Section ---
st.header("Your Saved Notes")

# Search and Category Filter Row
col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input("🔍 Search notes...", placeholder="Type to filter...", label_visibility="collapsed")
with col2:
    # This allows you to filter by category easily
    filter_cat = st.selectbox("Filter Category", options=["All"] + CATEGORIES)

# Filtering Logic
filtered_notes = st.session_state.notes

# Apply Category Filter first
if filter_cat != "All":
    filtered_notes = [n for n in filtered_notes if n.get("category") == filter_cat]

# Apply Search Filter second
if search_query:
    filtered_notes = [
        note for note in filtered_notes 
        if search_query.lower() in note["title"].lower() or search_query.lower() in note["content"].lower()
    ]

# --- Display Section ---
if not filtered_notes:
    st.info("No notes found matching your selection.")
else:
    st.write(f"Showing {len(filtered_notes)} note(s)")
    for idx, note in enumerate(filtered_notes):
        # Display a nice "Badge" for the category
        with st.expander(f"[{note.get('category', 'Uncategorized')}] {note['title']}"):
            st.write(note["content"])
            
            # Find the actual index in the main list to ensure we delete the correct one
            original_index = -1
            for i, n in enumerate(st.session_state.notes):
                if n["title"] == note["title"] and n["content"] == note["content"]:
                    original_index = i
                    break
            
            if original_index != -1:
                if st.button(f"Delete", key=f"del_{original_index}"):
                    # Remove the note from the session state list
                    st.session_state.notes.pop(original_index)
                    # Save the updated list to the JSON file
                    save_data(st.session_state.notes)
                    st.success("Note deleted.")
                    st.rerun()