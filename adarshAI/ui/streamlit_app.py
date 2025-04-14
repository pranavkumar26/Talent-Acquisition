import streamlit as st
from agents.sourcing_agent import sourcing
from agents.screening_agent import screening
from agents.engagement_agent import chat_bot
from agents.scheduling_agent import scheduler

st.set_page_config(page_title="AI Recruiter", layout="centered")
st.title("🤖 AI Recruitment Assistant")

if st.button("🚀 Start Pipeline"):
    st.info("🔍 Ingesting resumes...")
    sourcing.ingest_resumes()

    st.info("🎯 Screening candidates...")
    job_desc = st.text_area("📝 Enter Job Description:")
    if job_desc:
        resumes = screening.load_resumes()
        top_candidates = screening.match_candidates(job_desc, resumes)

        st.success("Top Candidates:")
        for i, c in enumerate(top_candidates, 1):
            st.write(f"{i}. {c['name']} - Score: {c['similarity']:.2f}")

        selected = st.selectbox("🧑 Select a candidate to chat with:", [c["name"] for c in top_candidates])
        
        if st.button("💬 Start Chat"):
            st.warning("Chat will open in the terminal...")
            chat_bot.chat_with_candidate()

        if st.button("📅 Schedule Interview"):
            date = st.date_input("Select Date")
            time = st.time_input("Select Time")
            scheduler.schedule_interview(selected, str(date), str(time))
            st.success(f"Interview scheduled with {selected}!")
