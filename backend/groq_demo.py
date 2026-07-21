from chatbot import get_ai_response

message = input("You: ")

reply = get_ai_response(message)

print("\nAssistant:", reply)