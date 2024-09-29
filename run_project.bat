@echo off
python -m venv .\.venv
cd .\.venv\Scripts
call activate
cd ..\..
pip install -r requirements.txt
python main.py
