from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
from django.conf import settings

config = {
    "apiKey": settings.FIREBASE_API_KEY,
    "authDomain": settings.FIREBASE_AUTH_DOMAIN,
    "databaseURL": settings.FIREBASE_DATABASE_URL,
    "projectId": settings.FIREBASE_PROJECT_ID,
    "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
    "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
    "appId": settings.FIREBASE_APPID,
    "measurementId": settings.FIREBASE_MEASUREMENT_ID
}
# Create your viefrom django.http import HttpResponse

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get(request):
    users = database.child("accounts").get().val()
    print("DB connected")
    print(users)
    return render(request, 'base.html', {
        "users": users
    })

def signup(request):
    username = "peter pan"
    password = "b"
    
    data = {"username": username, "password": password}
    database.child("accounts").push(data)
        
    return HttpResponse("sign up page")

def login(request):
    if request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        
        if not username or not password:
            return HttpResponse("Missing Info!")
        
        accounts = database.child("accounts").get().val()
            
        # Check if provided username and password match any account
        for key, val in accounts.items():
            if val['username'] == username and val['password'] == password:
                # Successful login
                return HttpResponse(f"Welcome, {username}!")

        return HttpResponse(f"log in failed!")

def delete(request):
    if request.method == 'GET':
        username_to_delete = request.GET.get('username')
        if not username_to_delete:
            return HttpResponse("Missing Info!")
        accounts = database.child("accounts").get().val()
        
        for key, account in accounts.items():
            if account['username'] == username_to_delete:
                # Delete the user
                database.child("accounts").child(key).remove()
                return HttpResponse("User deleted successfully.")
        
        
        return HttpResponse("user not found")
    
    return HttpResponse("Only DELETE requests are allowed for deletion.")
        
def changepassword(request):
    if request.method == "GET":
        username = request.GET.get("username")
        password = request.GET.get("password")
        if not username or not password:
            return HttpResponse("Missing Info!")
        
        accounts = database.child("accounts").get().val()
        
        for key, val in accounts.items():
            if val['username'] == username:
                val['password'] = password
                return HttpResponse("Password Changed! success")
        
        return HttpResponse("account not found!")  
    
    return HttpResponse("Only POST requests are allowed for change password.")