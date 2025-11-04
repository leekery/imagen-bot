from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router(name="star")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Команды: /start, /help, /echo")

@router.message(Command("echo"))
async def cmd_echo(message: Message):
    payload = message.text.removeprefix("/echo").strip() if message.text else ""
    await message.answer(payload or "Empty 0_o")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Welcome To The New York City!")