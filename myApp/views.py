from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterationForm, PostIncidentForm, PostPropertyForm, ChangePasswordForm
from django.http import JsonResponse
from .forms import LoginForm, RegisterationForm, PostIncidentForm, PostPropertyForm, ChangePasswordForm , EditDetailsForm
import pymongo
import math
from datetime import datetime
from threading import Thread
from passlib.hash import bcrypt_sha256
import bcrypt

client = pymongo.MongoClient("mongodb+srv://<username>:<password>@hostedprojectsdb.xggdbhg.mongodb.net/?retryWrites=true&w=majority")

db = client["CrimeAndHazardDB"]
user_collection = db["users"]
incident_collection = db["incident"]
property_collection = db["properties"]


def index(request):
    username = request.session.get('username')
    Thread(target=hourly_function).start()
    if username is not None:
        return render(request, 'myApp/reg_hmpg.html', {'user': username})
    else:
        return render(request, 'myApp/unreg_hmpg.html', {'user': None})


def login(request):
    if request.session.get('username') is not None:
        return redirect('/myApp')
    elif request.method == 'POST':
        (request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            query = {"UserName": form.UserName}
            projection = {"_id": 0, "UserName": 1, "Password": 1}

            user = user_collection.find_one(query, projection)
            if user is None:
                error_message = "Invalid username or password"
                return render(request, 'myApp/login.html', {'error_message': error_message})
            
            password = user['Password']
            verify=False
            try:
                verify = bcrypt_sha256.verify(form.Password, password)
            except:
                error_message = "Invalid username or password"
                return render(request, 'myApp/login.html', {'error_message': error_message})

            if verify==True:
                request.session['username'] = user['UserName']
                request.session.save()
                return redirect('/myApp')
            else:
                error_message = "Invalid username or password"
                return render(request, 'myApp/login.html', {'error_message': error_message})
        else:
            error_message = "Required fields are invalid or empty, please try again"
            return render(request, 'myApp/login.html', {'error_message': error_message})
    else:
        return render(request, 'myApp/login.html')


def register(request):
    if request.session.get('username') is not None:
        return redirect('/myApp')
    elif request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            if form.Password != form.ConfirmPassword:
                error_message = "Passwords do not match"
                return render(request, 'myApp/register.html', {'error_message': error_message})

            query = {"UserName": form.UserName}
            projection = {"_id": 0, "UserName": 1}

            user = user_collection.find_one(query, projection)

            if user is None:
                form.Password = bcrypt_sha256.hash(form.Password)
                user_collection.insert_one(form.to_dict())
                request.session['username'] = form.UserName
                request.session.save()
                return redirect('/myApp')
            else:
                error_message = "Username already exists"
                return render(request, 'myApp/register.html', {'error_message': error_message})
        else:
            error_message = "Required fields are invalid or empty, please try again"
            return render(request, 'myApp/register.html', {'error_message': error_message})
    else:
        return render(request, 'myApp/register.html')


def logout(request):
    request.session.flush()
    return redirect('/myApp')


def calc_distance(lat1, long1, lat2, long2):
    R = 6371  # Earth's radius in kilometers
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

def hourly_function():
    #This function will retrieve all the incidents present till current time
    #Also all properties present till the current time
    #It will create two dictionaries 'INC' and 'PROP', where all the respective data is stored
    #Next retrieve the needed data for incident = {longitude, latitude, time, coefficient}
    #Same goes for property = {longitude, latitude}
    # Call calculate_score

    incident_list = list(incident_collection.find())
    property_list = list(property_collection.find())
    calculate_score(property_list, incident_list)


def calculate_score(property_list, incident_list):
    #The function is based on following formula:
    # (SIGMA(Ci * exp(-k1 * ti) * exp(-k2 * di))) / SIGMA(Ci * exp(-k1 * ti)) * 100
    # di = distance difference
    # ti = time difference
    k1 = 1
    k2 = 1

    for property_data in property_list:
        longitude1 = property_data['longitude']
        latitude1 = property_data['latitude']
        prop_score = property_data['score']             # get score variable

        numerator = 0
        denominator = 0
        for incident_data in incident_list:
            longitude2 = incident_data['longitude']
            latitude2 = incident_data['latitude']
            coeff = incident_data['incident_type']
            thattime = incident_data['time']            # retrieve incident time
            postid = incident_data['post_ID']           # retrieve post id

            di = calc_distance(latitude1, longitude1, latitude2, longitude2)
            # calculate time difference ti
            current_time = datetime.utcnow().isoformat()
            curdt = datetime.fromisoformat(current_time)
            thatdt = datetime.fromisoformat(thattime)
            
            yeardiff = curdt.year - thatdt.year
            monthdiff = curdt.month - thatdt.month
            if (monthdiff < 0):
                yeardiff -= 1
                monthdiff += 12
            daydiff = curdt.day - thatdt.day
            if (daydiff < 0):
                monthdiff -= 1
                daydiff += 30
            hourdiff = curdt.hour - thatdt.hour
            if (hourdiff < 0):
                daydiff -= 1
                hourdiff += 24
            ti = yeardiff + monthdiff/12 + daydiff/30/12 + hourdiff/24/30/12    # May need to modify
            k2 = incident_data['incident_type']
            numerator += math.exp(-(ti+1e-12))*math.exp(-(di+1e-12))*1e10*k2    #removed coeff
        prop_score = (numerator)*100
        property_data['score'] = prop_score
        # store the score in the database for this property using property_id        
        # for prop_id, prop_score in property_list:
        #property_collection.update_one({'post_ID': property_data['post_ID']}, {'$set': {'score': prop_score}})
    property_list = sorted(property_list, key=lambda d: d['score'])
    length = len(property_list)
    for i in range(len(property_list)):
        property_list[i]['score'] = ((length - i*1.0)/length)*99.99999999999999999
    for property_data in property_list:
        property_collection.update_one({'post_ID': property_data['post_ID']}, {'$set': {'score': property_data['score']}})


def PostIncident(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):  
            form = PostIncidentForm(request.POST, username)
            if form.is_valid():
                incident_collection.insert_one(form.to_dict())
                return redirect('/myApp')
            else:
                error_message = "Required fields are invalid or empty, please try again."
                return render(request, 'myApp/PostIncident.html', {'user': username, 'error_message': error_message})
        else:
            return render(request, 'myApp/PostIncident.html', {'user': username})
    else:
        return redirect('/myApp/login/')


def PostProperty(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):
            form = PostPropertyForm(request.POST, username)
            if form.is_valid():
                property_collection.insert_one(form.to_dict())
                return redirect('/myApp')
            else:
                error_message = "Required fields are invalid or empty, please try again."
                return render(request, 'myApp/PostProperty.html', {'user': username, 'error_message': error_message})
        else:
            return render(request, 'myApp/PostProperty.html', {'user': username})
    else:
        return redirect('/myApp/login/')


def profile(request):
    username = request.session.get('username')
    if username is not None:
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/profile.html', {'user': user})
    else:
        return redirect('/myApp/login/')
    

def editprofile(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):
            form = EditDetailsForm(request.POST)
            if form.is_valid():
                user_collection.update_one({"UserName": username}, {"$set": form.to_dict()})
                return redirect('/myApp/profile/')
            else:
                return HttpResponse("Profile Update Failed")
        else:
            user = user_collection.find_one({"UserName": username})
            return render(request, 'myApp/EditDetails.html', {'user': user})
    else:
        return redirect('/myApp/login/')


def SeeProfiles(request, ProfileID):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            user = user_collection.find_one({"UserName": ProfileID})
            if user is not None:
                return render(request, 'myApp/SeeProfile.html', {'user': user, 'myuser': username})
            else:
                return HttpResponse("User does not exist")
    else:
        if (request.method == 'GET'):
            user = user_collection.find_one({"UserName": ProfileID})
            if user is not None:
                return render(request, 'myApp/SeeProfile.html', {'user': user})
            else:
                return HttpResponse("User does not exist")


def Upvote(request, PostID):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            query = {"post_ID": PostID}
            post = incident_collection.find_one(query)
            myuser = user_collection.find_one({"UserName": username})
            curr = post['upvotes'] - post['downvotes']
            downvoted = myuser['downvoted']
            upvoted = myuser['upvoted']
            if (post is None) or (downvoted.get(PostID) != None):
                return HttpResponse(status = 500)
            elif upvoted.get(PostID) != None:
                new_values = {"$set": {"upvotes": post['upvotes'] - 1}}
                incident_collection.update_one(query, new_values)
                upvoted.pop(PostID)
                new_values = {"$set": {"upvoted": upvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "neutral", "votes": curr-1})
            else:
                new_values = {"$set": {"upvotes": post['upvotes'] + 1}}
                incident_collection.update_one(query, new_values)
                upvoted[PostID] = True
                new_values = {"$set": {"upvoted": upvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "upvoted", "votes": curr+1})
    else:
        return redirect('/myApp/login/')


def find_post(PostID):
    query = {"post_ID": PostID}
    post = incident_collection.find_one(query)
    return post


def find_user(username):
    myuser = user_collection.find_one({"UserName": username})
    return myuser


def Downvote(requests, PostID):
    username = requests.session.get('username')
    if username is not None:
        if (requests.method == 'GET'):
            query = {"post_ID": PostID}
            post = find_post(PostID)
            curr = post['upvotes'] - post['downvotes']
            myuser = find_user(username)
            downvoted = myuser['downvoted']
            upvoted = myuser['upvoted']
            if (post is None) or (upvoted.get(PostID) != None):
                return HttpResponse(status = 500)
            elif downvoted.get(PostID) != None:
                new_values = {"$set": {"downvotes": post['downvotes'] - 1}}
                incident_collection.update_one(query, new_values)
                downvoted.pop(PostID)
                new_values = {"$set": {"downvoted": downvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "neutral", "votes": curr+1})
            else:
                new_values = {"$set": {"downvotes": post['downvotes'] + 1}}
                incident_collection.update_one(query, new_values)
                downvoted[PostID] = True
                new_values = {"$set": {"downvoted": downvoted}}
                user_collection.update_one({"UserName": username}, new_values)
                return JsonResponse({"status": "downvoted", "votes": curr-1})
    else:
        return redirect('/myApp/login/')


def Changepassword(request):
    username = request.session.get('username')
    if username is not None:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                query = {"UserName": form.UserName}
                user = user_collection.find_one(query)
                if user is None:
                    error_message = "User does not exist"
                    return render(request, 'myApp/changePassword.html', {'error_message': error_message,'myuser':username})
                else:
                    if user['DOB'] != form.DOB:
                        error_message = "Incorrect Date of Birth"
                        return render(request, 'myApp/changePassword.html', {'error_message': error_message,'myuser':username})
                    else:
                        query = {"UserName": form.UserName}
                        # form.new_password = bcrypt_sha256.encrypt(form.new_password)
                        form.new_password = bcrypt_sha256.hash(form.new_password)
                        # print(form.new_password)
                        new_values = {"$set": {"Password": form.new_password}}
                        user_collection.update_one(query, new_values)
                        return redirect('/myApp/profile/')
            else:
                error_message = "Required fields are invalid or empty, please try again"
                return render(request, 'myApp/changePassword.html', {'error_message': error_message,'myuser':username})
        else:
            return render(request, 'myApp/changePassword.html',{'myuser':username})
    else:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                query = {"UserName": form.UserName}
                user = user_collection.find_one(query)
                if user is None:
                    error_message = "User does not exist"
                    return render(request, 'myApp/changePassword.html', {'error_message': error_message})
                else:
                    if user['DOB'] != form.DOB:
                        error_message = "Incorrect Date of Birth"
                        return render(request, 'myApp/changePassword.html', {'error_message': error_message})
                    else:
                        query = {"UserName": form.UserName}
                        form.new_password = bcrypt_sha256.hash(form.new_password)
                        new_values = {"$set": {"Password": form.new_password}}
                        user_collection.update_one(query, new_values)
                        return redirect('/myApp/login/')
            else:
                error_message = "Required fields are invalid or empty, please try again"
                return render(request, 'myApp/changePassword.html', {'error_message': error_message})
        else:
            return render(request, 'myApp/changePassword.html')
    

def IncidentFeed(request):
    if (request.method == 'GET'):
        posts = list(incident_collection.find())
        username = request.session.get('username')
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/IncidentFeed.html', {'posts': posts, 'user': user, 'myuser':username})
    else:
        return HttpResponse("Error")
    

def PropertyFeed(request):
    if (request.method == 'GET'):
        posts = property_collection.find().sort("score", 1)
        username = request.session.get('username')
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/PropertyFeed.html', {'posts': posts, 'user': user, 'myuser':username})
    else:
        return HttpResponse("Error")
    

def SearchIncident(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):
            prompt = request.POST['prompt']
            posts = incident_collection.find({'$text': {'$search':prompt}},{ 'score': { '$meta': "textScore" } })
            posts.sort([('score', {'$meta': 'textScore'})])
            posts = list(posts)
            return render(request, 'myApp/IncidentFeed.html', {'posts': posts, 'myuser':username})
        else:
            return HttpResponse("Error")
    else:
        if (request.method == 'POST'):
            prompt = request.POST['prompt']
            posts = incident_collection.find({'$text': {'$search':prompt}},{ 'score': { '$meta': "textScore" } })
            posts.sort([('score', {'$meta': 'textScore'})])
            posts = list(posts)
            return render(request, 'myApp/IncidentFeed.html', {'posts': posts})
        else:
            return HttpResponse("Error")
    
    
def SearchProperty(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'POST'):
            prompt = request.POST['prompt']
            posts = property_collection.find({'$text': {'$search':prompt}},{ 'score': { '$meta': "textScore" } })
            posts.sort([('score', {'$meta': 'textScore'})])
            posts = list(posts)
            return render(request, 'myApp/PropertyFeed.html', {'posts': posts ,'myuser':username})
        else:
            return HttpResponse("Error")
    else:
        if (request.method == 'POST'):
            prompt = request.POST['prompt']
            posts = property_collection.find({'$text': {'$search':prompt}},{ 'score': { '$meta': "textScore" } })
            posts.sort([('score', {'$meta': 'textScore'})])
            posts = list(posts)
            return render(request, 'myApp/PropertyFeed.html', {'posts': posts})
        else:
            return HttpResponse("Error")
    

def myPost(request):
    username = request.session.get('username')
    if username is not None:
        if (request.method == 'GET'):
            posts = incident_collection.find({'author': username})
            posts = list(posts)
            return render(request, 'myApp/IncidentFeed.html', {'posts': posts, 'myuser':username})
        else:
            return HttpResponse("Error")
    else:
        return redirect('/myApp/login/')
    

def SeeIncident(request, PostID):
    username = request.session.get('username')
    if (request.method == 'GET'):
        post = incident_collection.find_one({'post_ID': PostID})
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/SeeIncident.html', {'post': post, 'user': user, 'myuser':username})
    else:
        return HttpResponse("Error")
    

def SeeProperty(request, PostID):
    username = request.session.get('username')
    if (request.method == 'GET'):
        post = property_collection.find_one({'post_ID': PostID})
        user = user_collection.find_one({"UserName": username})
        return render(request, 'myApp/SeeProperty.html', {'post': post, 'user': user, 'myuser':username})
    else:
        return HttpResponse("Error")
