from memory import ConversationMemory


def test_add_message():

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Hello"
    )

    assert len(memory.get_messages()) == 1


def test_clear_memory():

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Hi"
    )

    memory.clear()

    assert memory.is_empty()


def test_history_limit():

    memory = ConversationMemory()

    for i in range(20):

        memory.add_message(
            "user",
            str(i)
        )

    assert len(memory.get_messages()) <= 10