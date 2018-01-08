![GitHub Logo](/gem/web/static/logo.svg)

Application to improve GBC meeting experience

# Installation
Edit config.ini
```
[db]
host = mongodb_host
port = 27017
name = gem
```
Complie assets and seed a database
```
pip3 install -r requirements.txt
python3 ./tools/assets_compile.py
python3 ./install.py
```

# Development
Run development server
```
export FLASK_DEBUG=1
export FLASK_APP=main.py
flask run
```

Run watchdog to compile assets automatically
```
pip3 install watchdog
python3 ./tools/assets_watchdog.py
```
