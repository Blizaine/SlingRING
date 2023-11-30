@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS= --disable-safe-unpickle --xformers  --opt-sdp-attention --disable-nan-check --api --no-half-vae --listen --port 7860

CD C:\SDWebUI\sd.webui\webui
call webui.bat

pause