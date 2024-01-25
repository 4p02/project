from models import Register, Login, Summerize
from main import app

"""
Index route just returns a string for testing if the server is running
"""
@app.get("/")
def index():
    return "<h1>Index Page</h1>"

"""
Google oauth authentication
"""
@app.get("/auth/google")
def google():
    return "<h1>Google auth</h1>"

"""
Google oauth callback
"""
@app.get("/auth/google/callback")
def google_callback():
    return "<h1>Google auth callback</h1>"


"""
Register route takes in a form of email, password, and full name
"""
@app.post("/auth/register")
def register(form_data: Register):
    return f'<h1>Register Page {form_data.password} {form_data.email} {form_data.full_name}</h1>'

"""
Login route takes in a form of email and password
"""
@app.post("/auth/login")
def login(form_data: Login):
    return f'<h1>Login Page {form_data.password} {form_data.email}</h1>'

"""
Given a url, return a summary of the article
"""
@app.post("/summerize")
def summerize(form_data: Summerize):
    return f"<h1>Summerize Page {form_data.url} </h1>"


"""
Given a url, return a shortened url
"""
@app.post("/shorten")
def shorten(form_data: Summerize):
    return f"<h1>Shorten Page {form_data.url} </h1>"



