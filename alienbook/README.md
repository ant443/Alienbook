# Facebook-clone

## Description
A rough clone of Facebook.

## Motivation
Simply creating websites is a good way to further your skills as a web developer. 
However, the design stage can be a roadblock to someone more interested in web development than web design. In copying the design of an existing website, it allows us to skip the design stage and focus on what we enjoy.

## Installing
If you want to take a look, you will need python 3.5+.  
Download the app and navigate to Facebook-clone-master directory in a terminal/cmd.

(optional)Create and activate a virtual environment:  
```python3 -m venv venv```  
Windows: `source venv/scripts/activate`  
Linux: `source venv/bin/activate`

Get the projects dependencies: `pip install -r requirements.txt`  
Create a file called: app.db  
Create the database tables in app.db: `flask db upgrade`  
Run the app on a local development server: `flask run`  
Now open a browser and enter localhost:5000 in the address bar.  
When finished, stop the server: `ctrl+c`