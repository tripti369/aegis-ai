from chatbot import AIChatbot


def test_chatbot_creation():

    bot = AIChatbot()

    assert bot.get_mode() == "General"


def test_set_mode():

    bot = AIChatbot()

    bot.set_mode("Coding")

    assert bot.get_mode() == "Coding"


def test_invalid_mode():

    bot = AIChatbot()

import pytest

def test_invalid_mode():
    bot = AIChatbot()

    with pytest.raises(ValueError):
        bot.set_mode("Doctor")