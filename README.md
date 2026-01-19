Desk GUI – DEMO

Aplikace pro správu zaměstnanců a směn s možností importu dat z CSV, generování statistik a vizualizace směn.

Požadavky

Python 3.9+

MySQL 8+

Balíčky (viz requirements.txt):

mysql-connector-python

Poznámka: tkinter je součástí standardní instalace Pythonu, není nutné ho instalovat přes pip.

Nastavení databáze

V MySQL spusť SQL skript mujstul.sql (obsahuje tabulky, vztahy a views).

Ujisti se, že máš uživatele s přístupem k databázi a správnými právy.

Konfigurace

V projektu vytvoř soubor config.py:

# config.py
DB_CONFIG = {
"host": "localhost",
"user": "root",
"password": "root",
"database": "mujstul",  
}


Každý uživatel, který stáhne projekt, upraví hodnoty podle své instalace MySQL.

Instalace balíčků

Otevři terminál v kořenové složce projektu a spusť:

pip install -r requirements.txt

Spuštění aplikace

V terminálu:

python main.py


Aplikace se otevře v okně Tkinter.

Funkce aplikace

Správa zaměstnanců:

Přidávání, upravování a mazání zaměstnanců.

Import zaměstnanců z CSV.

Správa směn:

Přidávání, upravování a mazání směn.

Import směn z CSV.

Statistika:

Souhrnné statistiky zaměstnanců podle pozice.

Zobrazení počtu zaměstnanců a směn.

