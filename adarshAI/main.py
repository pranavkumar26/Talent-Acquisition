print("Main script started ✅ please wait few sec...")

from agents.sourcing_agent import sourcing
from agents.screening_agent import screening
from agents.engagement_agent import chat_bot
from agents.scheduling_agent import scheduler

def run_pipeline():
    print("=== Step 1: Ingesting Resumes ===")
    sourcing.ingest_resumes()

    print("\n=== Step 2: Screening Candidates ===")
    job_desc = input("Enter job description for screening: ")
    resumes = screening.load_resumes()
    top_candidates = screening.match_candidates(job_desc, resumes)

    print("\n🎯 Top Candidates:")
    for i, c in enumerate(top_candidates, 1):
        print(f"{i}. {c['name']} (Score: {c['similarity']:.2f})")

    print("\n=== Step 3: Engaging Top Candidate ===")
    selected = input("Enter candidate name to chat with: ")
    print(f"Starting chat with {selected}...\n")
    #chat_bot.chat_with_candidate()
    chat_bot.chat_with_candidate(selected)


    print("\n=== Step 4: Schedule Interview ===")
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM): ")
    scheduler.schedule_interview(selected, date, time)

if __name__ == "__main__":
    run_pipeline()