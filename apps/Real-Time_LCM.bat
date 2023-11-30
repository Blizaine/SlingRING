@echo off

cd C:\Users\YOURNAME\conda\RTLCM\Real-Time-Latent-Consistency-Model
call ".\venv\Scripts\activate"

set COMMANDLINE_ARGS= SAFETY_CHECKER=False 
uvicorn "app-controlnet:app" --host 0.0.0.0 --port 7860 --reload --ssl-keyfile=key.pem --ssl-certfile=certificate.pem

pause
