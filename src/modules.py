# src/modules.py
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.types import Message, KeyboardButtonText, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os
import logging
import sqlite3
import asyncio
