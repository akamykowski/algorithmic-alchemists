"""Streamlit HR dashboard for OnboardPro MVP."""
from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

import pandas as pd
import requests
import streamlit as st

API_DEFAULT = "http://localhost:8000"

st.set_page_config(page_title="OnboardPro HR Dashboard", layout="wide")
st.title("OnboardPro HR Dashboard")

st.sidebar.header("Configuration")
api_base_url = st.sidebar.text_input("FastAPI base URL", value=API_DEFAULT)

@st.cache_data(ttl=30)
def fetch_users(api_url: str) -> List[Dict[str, str]]:
    response = requests.get(f"{api_url}/users", timeout=10)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=30)
def fetch_tasks(api_url: str) -> List[Dict[str, str]]:
    response = requests.get(f"{api_url}/tasks", timeout=10)
    response.raise_for_status()
    return response.json()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Create New User")
    with st.form("create_user_form"):
        new_name = st.text_input("Name")
        new_email = st.text_input("Email")
        new_role = st.selectbox("Role", ["HR", "Hiring Manager", "New Hire", "IT", "Other"])
        submitted = st.form_submit_button("Create User")
    if submitted:
        try:
            payload = {"name": new_name, "email": new_email, "role": new_role}
            response = requests.post(f"{api_base_url}/users", json=payload, timeout=10)
            response.raise_for_status()
            st.success("User created successfully.")
            fetch_users.clear()
        except requests.HTTPError as error:
            st.error(f"Failed to create user: {error.response.text}")
        except requests.RequestException as exc:
            st.error(f"Request error: {exc}")

with col2:
    st.subheader("Create New Task")
    with st.form("create_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_due = st.date_input("Due Date", value=date.today())
        task_status = st.selectbox("Status", ["pending", "in_progress", "complete"])
        users_for_assignment = fetch_users(api_base_url)
        user_labels = [f"{user['name']} ({user['role']})" for user in users_for_assignment]
        selected_index = st.selectbox("Assign To", options=list(range(len(user_labels))), format_func=lambda idx: user_labels[idx] if user_labels else "No users available") if users_for_assignment else None
        create_task = st.form_submit_button("Create Task")
    if create_task:
        try:
            assigned_user = users_for_assignment[selected_index]["id"] if users_for_assignment else None
            payload = {
                "title": task_title,
                "description": task_description,
                "due_date": task_due.isoformat() if isinstance(task_due, date) else None,
                "status": task_status,
                "user_id": assigned_user,
            }
            response = requests.post(f"{api_base_url}/tasks", json=payload, timeout=10)
            response.raise_for_status()
            st.success("Task created successfully.")
            fetch_tasks.clear()
        except requests.HTTPError as error:
            st.error(f"Failed to create task: {error.response.text}")
        except requests.RequestException as exc:
            st.error(f"Request error: {exc}")

st.markdown("---")

users_data: List[Dict[str, str]] = []
tasks_data: List[Dict[str, str]] = []
try:
    users_data = fetch_users(api_base_url)
    tasks_data = fetch_tasks(api_base_url)
except requests.RequestException as exc:
    st.warning(f"Could not load data from API: {exc}")

overview_col1, overview_col2, overview_col3 = st.columns(3)

with overview_col1:
    st.metric("Total Users", len(users_data))

with overview_col2:
    st.metric("Total Tasks", len(tasks_data))

with overview_col3:
    completed = sum(1 for task in tasks_data if task.get("status") == "complete")
    completion_rate = f"{(completed / len(tasks_data) * 100):.0f}%" if tasks_data else "0%"
    st.metric("Tasks Completed", completion_rate)

st.subheader("Users")
if users_data:
    st.dataframe(pd.DataFrame(users_data))
else:
    st.info("No users available. Create one using the form above.")

st.subheader("Tasks")
if tasks_data:
    tasks_df = pd.DataFrame(tasks_data)
    tasks_df["due_date"] = pd.to_datetime(tasks_df["due_date"])
    st.dataframe(tasks_df)
else:
    st.info("No tasks found. Use the form to create tasks.")

st.subheader("Task Breakdown by Status")
if tasks_data:
    status_counts = pd.DataFrame(tasks_df["status"].value_counts()).reset_index()
    status_counts.columns = ["Status", "Count"]
    st.bar_chart(status_counts.set_index("Status"))
else:
    st.info("Task breakdown will appear once tasks are created.")
