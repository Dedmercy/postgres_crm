@echo off

chcp 65001

SET server=localhost

SET database=postgres

SET port=5431

SET username=postgres

REM Run psql
"C:\2Programs\PostgreSQL\bin\psql.exe" -h %server% -U %username% -d %database% -p %port% -f insert.sql

pause