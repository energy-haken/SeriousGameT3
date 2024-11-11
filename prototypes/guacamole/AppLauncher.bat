@echo off

echo Lancement en cours, ne paniquez pas.
echo Tous vos mots de passe sont nous appartient.

SET CURRENTDIR="%~dp0"

cmd /k "cd /d %CURRENTDIR%\.venv\Scripts & .\activate & cd /d %CURRENTDIR% & python .\main.py"