import streamlit as st
import requests
import time

# Backend configuration
# API_BASE_URL = "http://localhost:8000/api/v1"
import os
# from dotenv import load_dotenv

# load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(
    page_title="YouTube Clipper",
    layout="centered"
)

st.title("🎬 YouTube Clipper")
st.write("Create precise clips from YouTube videos")

# -----------------------------
# Input Form
# -----------------------------
with st.form("clip_form"):
    youtube_url = st.text_input("YouTube URL")
    start_time = st.number_input(
        "Start Time (seconds)",
        min_value=0.0,
        value=0.0,
        step=0.1
    )
    end_time = st.number_input(
        "End Time (seconds)",
        min_value=0.1,
        value=10.0,
        step=0.1
    )

    submit = st.form_submit_button("Create Clip")

# -----------------------------
# Submit Job
# -----------------------------
if submit:
    if not youtube_url:
        st.error("Please enter a YouTube URL")
    elif end_time <= start_time:
        st.error("End time must be greater than start time")
    else:
        with st.spinner("Submitting clip job..."):
            response = requests.post(
                f"{API_BASE_URL}/clip",
                json={
                    "youtube_url": youtube_url,
                    "start_time": start_time,
                    "end_time": end_time
                }
            )

        if response.status_code != 200:
            st.error("Failed to create clip job")
        else:
            job_id = response.json()["job_id"]
            st.session_state["job_id"] = job_id
            st.success(f"Job created: {job_id}")

# -----------------------------
# Poll Job Status
# -----------------------------
if "job_id" in st.session_state:
    job_id = st.session_state["job_id"]

    st.divider()
    st.subheader("📊 Processing Status")

    progress_bar = st.progress(0)
    status_text = st.empty()

    while True:
        res = requests.get(f"{API_BASE_URL}/clip/{job_id}")
        data = res.json()

        progress = data.get("progress", 0)
        if progress is None:
            progress = 0

        status = data["status"]
        message = data.get("status_message") or "Initializing..."

        progress_bar.progress(int(progress))
        status_text.write(message)

        if status == "COMPLETED":
            st.success("🎉 Clip ready")
            st.download_button(
                "⬇️ Download Clip",
                data=requests.get(data["download_url"]).content,
                file_name="clip.mp4",
                mime="video/mp4"
            )
            break

        if status == "FAILED":
            st.error(f"❌ {data['error_message']}")
            st.info("⚠️ Free tier allows up to 20 MB per clip")
            break

        time.sleep(2)
