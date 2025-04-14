from datetime import datetime

calendar = {
    "2025-04-11": ["10:00", "14:00"],
    "2025-04-12": ["11:00", "15:00"],
}

def get_available_slots(date):
    return calendar.get(date, [])

def schedule_interview(candidate_name, date, time):
    if time in get_available_slots(date):
        print(f"✅ Interview scheduled for {candidate_name} on {date} at {time}")
        return True
    else:
        print("❌ Slot not available. Try another time.")
        return False

if __name__ == "__main__":
    candidate = "Alice Sharma"
    date = "2025-04-11"
    time = "10:00"
    schedule_interview(candidate, date, time)