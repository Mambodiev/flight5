source env/bin/activate
python3 manage.py runserver 


cd frontend
npm run start




pip install -r requirements.txt 
pip freeze > requirements.txt

python3 manage.py makemigrations    
python3 manage.py migrate 

git init
git add .
git commit -m "partially done with order detail"
git push -f