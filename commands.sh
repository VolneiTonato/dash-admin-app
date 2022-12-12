python3 -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt

python pyapp/app.py --command=drop-db
python pyapp/app.py --command=create-db
python pyapp/app.py --command=populate-db

python pyapp/app.py


localhost:8050

username: administrator
pass: 123

