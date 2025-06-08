from app.chatbot import get_bot_response

print("📘 Welcome to the JIIT Chatbot (CLI Mode). Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Bye! 👋")
        break

    response, intent = get_bot_response(user_input)
    print(f"Bot ({intent}): {response}")
