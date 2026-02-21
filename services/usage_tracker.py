from tinydb import TinyDB, Query
import uuid
import streamlit as st
import os

# Ensure data directory exists (important for cloud)
os.makedirs("data", exist_ok=True)

db = TinyDB("data/usage.json")
Users = Query()


def get_user_id():
    if "persistent_user_id" not in st.session_state:
        st.session_state.persistent_user_id = str(uuid.uuid4())
    return st.session_state.persistent_user_id


def has_used_free(user_id):
    return len(db.search(Users.id == user_id)) > 0


def mark_used(user_id):
    if not has_used_free(user_id):
        db.insert({"id": user_id})