import pytest
from aiogram import Bot

from aiogram_pytest.args_parser import ArgumentsParser
from aiogram_pytest.utils import initialize_bot


@pytest.fixture(name='bot')
def bot():
    return initialize_bot()


@pytest.mark.asyncio
async def test_converting(bot: Bot):
    await bot.send_message(chat_id=12345678, text="Hello, Bot!", parse_mode="Markdown")
    args = ArgumentsParser.get_send_message_args(bot.send_message.call_args)
    assert args.as_dict() == {
        "chat_id": 12345678,
        "text": "Hello, Bot!",
        "parse_mode": "Markdown",
        "entities": None,
        "disable_web_page_preview": None,
        "disable_notification": None,
        "protect_content": None,
        "reply_to_message_id": None,
        "allow_sending_without_reply": None,
        "reply_markup": None,
        "payload": None,
        "result": None,
    }


@pytest.mark.asyncio
async def test_converting_with_none(bot: Bot):
    args = ArgumentsParser.get_send_message_args(None)
    assert args.as_dict() == {
        "chat_id": None,
        "text": None,
        "parse_mode": None,
        "entities": None,
        "disable_web_page_preview": None,
        "disable_notification": None,
        "protect_content": None,
        "reply_to_message_id": None,
        "allow_sending_without_reply": None,
        "reply_markup": None,
        "payload": None,
        "result": None,
    }


@pytest.mark.asyncio
async def test_converting_with_incorrect_args(bot: Bot):
    await bot.send_message(arg1="arg1", arg2="arg2")
    args = ArgumentsParser.get_send_message_args(bot.send_message.call_args)
    assert args.as_dict() == {
        "chat_id": None,
        "text": None,
        "parse_mode": None,
        "entities": None,
        "disable_web_page_preview": None,
        "disable_notification": None,
        "protect_content": None,
        "reply_to_message_id": None,
        "allow_sending_without_reply": None,
        "reply_markup": None,
        "payload": None,
        "result": None,
    }
