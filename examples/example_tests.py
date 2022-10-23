from test_bot import callback_query_handler
from test_bot import callback_query_handler_with_state
from test_bot import command_handler
from test_bot import message_handler
from test_bot import message_handler_with_state
from test_bot import message_handler_with_state_data
from test_bot import States
from test_bot import test_callback_data

from aiogram_pytest import Requester
from aiogram_pytest.handler import CallbackQueryHandler
from aiogram_pytest.handler import MessageHandler
from aiogram_pytest.types.dataset import CALLBACK_QUERY
from aiogram_pytest.types.dataset import MESSAGE

import pytest


@pytest.mark.asyncio
async def test_message_handler():
    requester = Requester(request_handler=MessageHandler(message_handler))
    calls = await requester.query(MESSAGE.as_object(text="Hello!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello!"


@pytest.mark.asyncio
async def test_command_handler():
    requester = Requester(request_handler=MessageHandler(command_handler, commands=["start"]))
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, new user!"


@pytest.mark.asyncio
async def test_message_handler_with_state():
    requester = Requester(request_handler=MessageHandler(message_handler_with_state, staet=States.state))
    calls = await requester.query(MESSAGE.as_object(text="Hello, bot!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, from state!"


@pytest.mark.asyncio
async def test_callback_query_handler():
    requester = Requester(request_handler=CallbackQueryHandler(callback_query_handler, test_callback_data.filter()))

    callback_query = CALLBACK_QUERY.as_object(
        data=test_callback_data.new(id="1", name="John"), message=MESSAGE.as_object(text="Hello world!")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone().text
    assert answer_text == "Hello, John"

    callback_query = CALLBACK_QUERY.as_object(
        data=test_callback_data.new(id="1", name="Mike"), message=MESSAGE.as_object(text="Hello world!")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone().text
    assert answer_text == "Hello, Mike"


@pytest.mark.asyncio
async def test_callback_query_handler_with_state():
    requester = Requester(
        request_handler=CallbackQueryHandler(callback_query_handler_with_state, test_callback_data.filter()))

    callback_query = CALLBACK_QUERY.as_object(data=test_callback_data.new(id="1", name="John"))
    calls = await requester.query(callback_query)

    answer_text = calls.answer_callback_query.fetchone().text
    assert answer_text == "Hello, from state!"


@pytest.mark.asyncio
async def test_handler_with_state_data():
    requester = Requester(
        request_handler=MessageHandler(
            message_handler_with_state_data, state=States.state_1, state_data={"info": "this is message handler"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Info from state data: this is message handler"
