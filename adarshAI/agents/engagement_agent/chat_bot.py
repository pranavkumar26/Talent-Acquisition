# agents/engagement_agent/chat_bot.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer once
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.eos_token_id

# Interview-style starter questions
starter_questions = [
    "Tell me about yourself.",
    "What are your biggest strengths?",
    "Why do you want to work in this role?",
    "Can you describe a recent project you worked on?",
    "Do you have any questions for us?"
]

def chat_with_candidate(name="Candidate"):
    print(f"\n💬 Chatbot: Hello {name}, I'm your virtual interviewer today! Let's begin. Type 'exit' to finish.\n")

    chat_history_ids = None
    prev_attention_mask = None
    transcript = []

    for q in starter_questions:
        print(f"🤖 Bot: {q}")
        user_input = input("🧑 You: ")

        if user_input.lower() == "exit":
            print("👋 Chat ended early by user.")
            break

        transcript.append(f"You: {user_input}")

        # Prepare input
        encoded_input = tokenizer(user_input + tokenizer.eos_token, return_tensors='pt', padding=True)
        new_input_ids = encoded_input["input_ids"]
        attention_mask = encoded_input["attention_mask"]

        # Combine with history
        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
            attention_mask = torch.cat([prev_attention_mask, attention_mask], dim=-1)
        else:
            bot_input_ids = new_input_ids

        # Generate bot response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            attention_mask=attention_mask,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.8
        )

        prev_attention_mask = attention_mask

        # Decode bot response
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"🤖 Bot: {response}")
        transcript.append(f"Bot: {response}")

    print("\n📋 Chat Summary:")
    for line in transcript:
        print(line)

    # Optional: Save to file
    with open(f"{name.replace(' ', '_')}_chat.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(transcript))
    print(f"\n🗂️ Chat saved to {name.replace(' ', '_')}_chat.txt")
