# # from memory import ConversationMemory

# # memory = ConversationMemory()

# # memory.add_message("user", "Hello")
# # memory.add_message("assistant", "Hi!")

# # print(memory.get_messages())
# # print(memory.message_count())

# # memory.clear()

# # print(memory.get_messages())

# from prompts import build_messages

# history = [
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello!"}
# ]

# messages = build_messages(
#     user_message="Explain Python.",
#     history=history,
#     mode="Study"
# )

# for message in messages:
#     print(message)