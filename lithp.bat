@ECHO OFF

cd python
IF "%1"=="" GOTO BLANK
python lithp_evaluator.py ../%1
GOTO END

:BLANK
python lithp_evaluator.py

:END
cd ..