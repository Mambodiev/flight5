
pip install -r requirements.txt 
pip freeze > requirements.txt


source env/bin/activate
python3 manage.py runserver 


cd frontend
npm run start


python3 manage.py makemigrations    
python3 manage.py migrate 

git init
git add .
git commit -m "add to cart feature added"
git push -f