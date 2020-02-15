# Facebook-clone
A work in progress

If you want to take a look, you will need python 3.5+.  
Download the app and navigate to facebook-clone-master directory in a terminal/cmd.

(optional)Create and activate a virtual environment:  
```python3 -m venv venv```  
Windows: `source venv/scripts/activate`  
Linux: `source venv/bin/activate`

Get the projects dependencies: `pip install -r requirements.txt`  
Create a file: app.db  
Create the database tables in app.db: `flask db upgrade`  
Tell flask where to find the application: `export FLASK_APP=microblog.py`  
Run the app on a local development server: `flask run`  
Now open a browser and enter localhost:5000 in the address bar.
