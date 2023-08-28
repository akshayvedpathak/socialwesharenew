from django.shortcuts import HttpResponse,render,redirect
from Admin.models import Userinfo,userpost,followers 
from User.functions import handle_uploaded_file 
from datetime import datetime 
from django.core.mail import send_mail
from django.conf import settings
import re
import os
import csv
from pathlib import Path
import random
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def hellouser(request):
    return HttpResponse ('User/Hello user')

'''def login(request):
    return render(request,"User/login.html",{})'''



def get_location_data(ip_address):
    csv_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv')
    
    # Determine if the IP address is IPv4 or IPv6
    is_ipv4 = '.' in ip_address
    is_ipv4 = '.' in ip_address
    print("IP Address:", ip_address)
    print("Is IPv4:", is_ipv4)
    
    csv_filename = 'GeoLite2-City-Blocks-IPv4.csv' if is_ipv4 else 'GeoLite2-City-Blocks-IPv6.csv'
    print("CSV Filename:", csv_filename)
    csv_filename = 'GeoLite2-City-Blocks-IPv4.csv' if is_ipv4 else 'GeoLite2-City-Blocks-IPv6.csv'
    
    # Dictionary to map location IDs to human-readable location names
    location_names = {}
    with open(os.path.join(csv_directory, 'GeoLite2-City-Locations-en.csv'), 'r', encoding='utf-8') as loc_file:
        loc_reader = csv.reader(loc_file)
        for row in loc_reader:
            location_names[row[0]] = row[10]
    
    # Retrieve location data for the given IP address
    with open(os.path.join(csv_directory, csv_filename), 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if is_ipv4 and row[0] <= ip_address <= row[1]:
                return {
                    'city': location_names.get(row[2], 'Unknown'),
                    'country': location_names.get(row[3], 'Unknown')
                }
            elif not is_ipv4 and row[0] <= ip_address <= row[1]:
                return {
                    'city': location_names.get(row[2], 'Unknown'),
                    'country': location_names.get(row[3], 'Unknown')
                }
    return {
        'city': 'Unknown',
        'country': 'Unknown'
    }

# Usage
# ip_address = '203.0.113.45'  # Replace with the user's IP address
# location_data = get_location_data(ip_address)
# print("City:", location_data['city'])
# print("Country:", location_data['country'])


def login(request):
    '''forwarded_ips = request.META.get('HTTP_X_FORWARDED_FOR')
    user_ip = forwarded_ips.split(',')[-1].strip() if forwarded_ips else request.META.get('REMOTE_ADDR', None)
    user_ip="182.69.218.81"
    #print(type(user_ip))
    location_data = get_location_data(user_ip)
    print(location_data)
    print("City:", location_data['city'])
    print("Country:", location_data['country'])'''
    return render(request,"User/login.html",{})

def register(request):
    return render(request,"User/signup.html",{})

def info(request):
    if(request.method == "GET"):
        return render(request,"User/signup.html",{})
    else:
        # Add more words as needed
        banned_words = ["fuck", "sex", "sexy", "dick", "pussy"]
        

        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        bday = request.POST["bday"]
        location = request.POST["location"]


         # Define a regular expression pattern for banned words
        banned_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in banned_words) + r')\b', re.IGNORECASE)

        # Check for banned words in fname and lname using the regular expression pattern
        if banned_pattern.search(fname) or banned_pattern.search(lname) or banned_pattern.search(email) or banned_pattern.search(location):
            error_message = "Sorry, but the name you entered contains inappropriate words. Please provide a respectful name."
            return render(request, "User/signup.html", {"error_message": error_message})

        print(fname,lname,email,password,phone,bday,location)
        user = Userinfo()
        user.fname = fname
        user.lname = lname
        user.email = email
        user.password = password
        user.phone = phone
        user.bday = bday
        user.location = location
        user.save()
        print("save")
        request.session["email"]=email
        return render(request,"User/info.html",{"fname":fname})

def successfull(request):
    if("email" in request.session):
        email = request.session["email"]
        print(email)
        print("succesful")
        profile =request.FILES['profil']
        cover =request.FILES['cover']
        '''handle_uploaded_file(request.FILES['profil'])
        print("--------------",handle_uploaded_file(request.FILES['profil']))
        handle_uploaded_file(request.FILES['cover'])
        print("--------------",handle_uploaded_file(request.FILES['cover']))'''
        handle_uploaded_file((profile))
        handle_uploaded_file((cover))

        #profile =request.FILES['profil']
        print("profile url- ",profile)
        print("cover url",cover)
        #cover =request.FILES['cover']
        Bio =request.POST["Bio"]
        user = request.session["email"]
        user = Userinfo.objects.get(email=user)
        print("object fetched")
        user.profil=profile
        user.cover=cover
        user.Bio=Bio
        user.save()
        print(email)
        print("--",settings.EMAIL_HOST_USER)
        msg = """
        Hello,

        Welcome to WeShare. We are Happy to see you here!

        We are confident that WeShare will help you to 
        connect people and much more.

        You can also Post it Here with your beautiful Images.

        Have a Good Day ahead..!

        
        
        Thank You,
        WeShare Community.
        """
        #below code is used for sending mail
        send_mail("Welcome to WeShare",msg,'settings.EMAIL_HOST_USER',[email],fail_silently=False)
        #after signup direct user can see login page
        suggetion = []
        try:
            user = Userinfo.objects.get(email=email)
        except:
            return render(request,"login.html",{}) 
        else:
            
            data = str((user.joining))
            data = data[0:11]
            print("joining date : ",data)
            users = Userinfo.objects.all()
            for i in users:

                if(str(i.email) == email):
                    continue
                else:
                    suggetion.append(i)

            users = suggetion
            return render(request,"User/home.html",{"user":user,"joiningtime":data,"all":users})
    else:
        return render(request,"User/login.html",{})  
            
def home(request):
    if(request.method == "GET"):
        if "email" in request.session:
            email=request.session["email"]
            useremail = request.session["email"]
            
            try:
                user = Userinfo.objects.get(email=email)
            except:
                return render(request,"login.html",{}) 
            else:
              
                joiningtime = str((user.joining))
                joiningtime = joiningtime[0:11]
                print("joining date : ",joiningtime)

                post = userpost.objects.filter(user_id=user)
                
                user = Userinfo.objects.get(email = useremail)
    
                datass = followers.objects.filter(user_id=user)
                new = []
                new1 = []
                for i in datass:
                    new.append(i.frinds)
                print(new)
                for x in new:
                    myfriends = Userinfo.objects.get(id = x)
                    print(str(myfriends))
                    new1.append(myfriends)
                print(new1)
                size = len(new1)

                suggetion_for_you = []
                
                alluser = Userinfo.objects.all()
                print("All user:-",alluser)
                for i in alluser:
                    print(i.email)
                    print(i)
                    if(str(i.email) == useremail) or (i in new1):
                        print("********")
                        continue
                    else:
                        suggetion_for_you.append(i)
                return render(request,"User/home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":suggetion_for_you,"size":size})
            
        else:

            return render(request,"User/login.html",{})
    else:
        email =request.POST["email"]
        password =request.POST["password"]
        request.session["email"]=email
        suggetion = []

        #to get user ip address
        forwarded_ips = request.META.get('HTTP_X_FORWARDED_FOR')
        user_ip = forwarded_ips.split(',')[-1].strip() if forwarded_ips else request.META.get('REMOTE_ADDR', None)
        #print("user ip",user_ip)
        try:
            user = Userinfo.objects.get(email=email,password=password)
        except:
            return render(request,"User/login.html",{}) 
        else:
            x = ''
            joiningtime = str((user.joining))
            joiningtime = joiningtime[0:11]
            print("joining date : ",joiningtime)

            post = userpost.objects.filter(user_id=user)
            
            users = Userinfo.objects.all()
            for i in users:
                if(str(i.email) == email):
                    continue
                else:
                    suggetion.append(i)
            users = suggetion
            current_time = datetime.now()
            log_entry = f"{current_time}: User with email '{email}' with the ip '{user_ip}' logged in.\n"
    
            with open("login_log.txt", "a") as log_file:
                log_file.write(log_entry)
            return render(request,"User/home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":users})
            
def logout(request):
    email=request.session["email"]
    current_time = datetime.now()
    #to get user ip address
    forwarded_ips = request.META.get('HTTP_X_FORWARDED_FOR')
    user_ip = forwarded_ips.split(',')[-1].strip() if forwarded_ips else request.META.get('REMOTE_ADDR', None)
    #print("user ip",user_ip)
    logout_entry = f"{current_time}: User with email '{email}' with the ip '{user_ip} logged out.\n"
    with open("logout_log.txt", "a") as log_file:
        log_file.write(logout_entry)

    request.session.clear()
    return redirect(login)

def addpost(request):
    print("***************************************************")
    if "email" in request.session:
        useremail = request.session["email"]
        
        user = Userinfo.objects.get(email=useremail)
        
        caption = request.POST["caption"]
        print(caption)
        handle_uploaded_file(request.FILES['postphoto'])
        postphoto =request.FILES['postphoto']
        print(postphoto)
        post = userpost()
        post.caption = caption
        post.postphoto = postphoto
        post.user = user
        post.save()
        joiningtime= str(post.posttime)
        joiningtime = joiningtime[0:16]
        print("save")
        users = Userinfo.objects.all()
        datas = userpost.objects.filter(user_id=user)
        print(datas,"****************************")

        user = Userinfo.objects.get(email = useremail)
    
        datass = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datass:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
        
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        return render(request,"User/home.html",{"user":user,"datas":datas,"joiningtime":joiningtime,"all":suggetion_for_you})

def about(request):
    useremail = request.session["email"]
    print(useremail)
    user = Userinfo.objects.get(email = useremail)
    print(user)
    post = userpost.objects.filter(user_id=user)
    
    joiningtime = str((user.joining))
    joiningtime = joiningtime[0:11]
    '''suggetion = []
    alluser = Userinfo.objects.all()
    for i in alluser:

        if(str(i.email) == useremail):
            continue
        else:
            suggetion.append(i)'''


    user = Userinfo.objects.get(email = useremail)
    
    datass = followers.objects.filter(user_id=user)
    new = []
    new1 = []
    for i in datass:
        new.append(i.frinds)
    print(new)
    for x in new:
        myfriends = Userinfo.objects.get(id = x)
        print(str(myfriends))
        new1.append(myfriends)
    print(new1)
    size = len(new1)

    suggetion_for_you = []
    
    alluser = Userinfo.objects.all()
    print("All user:-",alluser)
    for i in alluser:
        print(i.email)
        print(i)
        if(str(i.email) == useremail) or (i in new1):
            print("********")
            continue
        else:
            suggetion_for_you.append(i)
    print(alluser)
    print(suggetion_for_you)
    return render(request,"User/about.html",{"user":user,"all":suggetion_for_you,"datas":post,"joiningtime":joiningtime,"size":size})

def timeline(request):
    if "email" in request.session:
        useremail = request.session["email"]
        print(useremail)
        user = Userinfo.objects.get(email=useremail)
        print(user)
        post = userpost.objects.filter(user_id=user)
        print(post)
        
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        '''suggetion = []
        alluser = Userinfo.objects.all()
        for i in alluser:

            if(str(i.email) == useremail):
                continue
            else:
                suggetion.append(i)'''
        user = Userinfo.objects.get(email = useremail)
        
        datass = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datass:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        
        
        

        
        return render(request,"User/home.html",{"user":user,"datas":post,"all":suggetion_for_you,"joiningtime":joiningtime,"size":size})

def photos(request):
    if "email" in request.session:
        
        useremail = request.session["email"]
        user = Userinfo.objects.get(email = useremail)
        post = userpost.objects.filter(user_id=user)
        alluser = Userinfo.objects.all()
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]

        user = Userinfo.objects.get(email = useremail)
        
        datass = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datass:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)


        return render(request,"User/photos.html",{"datas":post,"user":user,"all":suggetion_for_you,"joiningtime":joiningtime,"size":size})

def friends(request,id):
    if "email" in request.session:
        
        useremail = request.session["email"]
        user = Userinfo.objects.get(email = useremail)
        post = userpost.objects.filter(user_id=id)
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        user = Userinfo.objects.get(email = useremail)
        
        datas = followers.objects.filter(user_id=user)
        new = []
        new1 = []
        for i in datas:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
       
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        following = followers.objects.filter(user_id=user)

        #for my frinds section
        friend = []
        final_friend=[]
        for i in following:
            friend.append(i)
            print("My following",i.frinds)
        for y in friend:

            frinds = Userinfo.objects.get(id = y.frinds)
            final_friend.append(frinds)
        print("my final frinds id: -",final_friend)

        return render(request,"User/following.html",{"user":user,"all":suggetion_for_you,"datas":post,"size":size,"joiningtime":joiningtime,"following":final_friend})
    
def forgot(request):
    return render(request,"User/forgot.html",{})

def updatepassword(request):
    if request.method == 'GET':
        return render(request,"User/forgot.html",{})
    else:
        
        email = request.POST["email"]
        phone = request.POST["phone"]
        print(email)
        print(phone)
        try:

            user= Userinfo.objects.get(email=email,phone=phone)
            print("archived")
            
        except:
            return render(request,"User/forgot.html",{})
        else:
            fname = user.fname
            lname = user.lname
            global otp
            otp = random.randint(0000,9999)
            msg = ('Hello {0} {1},  \n\nThis email is to confirm that you requested a password reset.\nTo complete the password reset process, Use bloew OTP. \n\nOTP: {2}'.format(fname,lname,otp))

            #below code is used for sending mail
            send_mail("RESET",msg,'settings.EMAIL_HOST_USER',[email],fail_silently=False)
            request.session["email"]=email
            return render(request,"User/changepassword.html",{"user":user})

def save(request):
    if "email" in request.session:
        userotp = int(request.POST["otp"])

        original = int(otp)
        print(otp)
        print(userotp)
        if(original == userotp):
            print("both the conditions verified")
            return render(request,"User/finalpassword.html",{})
        else:
            return render(request,"User/changepassword.html",{})
        
    else:
        return render(request,"User/login.html",{})
    
def finalpass(request):
    if "email" in request.session:
        useremail = request.session["email"]
        enter = request.POST["enter"]
        re_enter = request.POST["re-enter"]
        if (enter == re_enter):
            user = Userinfo.objects.get(email =useremail)
            user.password = enter
            user.save()
            return redirect(login)
        else:
            return render(request,"User/login.html",{})

def following(request,id):
    #if(request.method == "post"):
    if "email" in request.session:
        print(id)
        
        useremail = request.session["email"]
        user = Userinfo.objects.get(email = useremail)
        post = userpost.objects.filter(user_id=id)
        print(len(post))
        print("posts:- ",post)
        print(user)
        print(id)
        print("*******************************************",id)
        f1 = followers()
        f1.user = user
        f1.frinds = id
        print("-------------------------------------------------------",f1)
        f1.save()
        
        joiningtime = str((user.joining))
        joiningtime = joiningtime[0:11]
        user = Userinfo.objects.get(email = useremail)
        
        myfriends = followers.objects.filter(user_id=user)
        print("-------------------------------",myfriends,"------------")
        new = []
        new1 = []
        for i in myfriends:
            new.append(i.frinds)
        print(new)
        for x in new:
            myfriends = Userinfo.objects.get(id = x)
            print(str(myfriends))
            new1.append(myfriends)
        print(new1)
        size = len(new1)

        suggetion_for_you = []
    
        alluser = Userinfo.objects.all()
        print("All user:-",alluser)
        for i in alluser:
            print(i.email)
            print(i)
            if(str(i.email) == useremail) or (i in new1):
                print("********")
                continue
            else:
                suggetion_for_you.append(i)
        print(alluser)
        print(suggetion_for_you)
        following = followers.objects.filter(user_id=id)


        friend = []
        final_friend=[]
        for i in following:
            friend.append(i)
            print("My following",i.frinds)
        for y in friend:

            frinds = Userinfo.objects.get(id = y.frinds)
            final_friend.append(frinds)
        print("my final frinds id: -",final_friend)


        return render(request,"User/following.html",{"user":user,"friends":new1,"datas":post,"all":suggetion_for_you,"size":size,"joiningtime":joiningtime,"following":final_friend})

    
def editprofile(request,id):
    user= Userinfo.objects.get(id = id)
    bday = str(user.bday)
    bday = bday[:10:]
    return render(request,"User/editprofile.html",{"user":user,"bday":bday})

def edited(request,id):

    if("email" in request.session):
        email = request.session["email"]
        user = Userinfo.objects.get(id = id)
        
        profil = user.profil
        cover= user.cover
        user.fname =request.POST["fname"]
        user.lname =request.POST["lname"]
        user.email =request.POST["email"]
        user.password =request.POST["password"]
        user.phone =request.POST["phone"]
        user.location =request.POST["location"]
        user.bday =request.POST["bday"]
        
        try:
            try:
                handle_uploaded_file(request.FILES['profil'])
                user.profil = request.FILES['profil']

                
                
            except:
                user.profil =profil
                

            try:

                handle_uploaded_file(request.FILES['cover'])
                
                user.cover =request.FILES['cover']
                    
            except:
                user.cover =cover
                   

        except:
            user.profil =profil
            user.cover =cover
            
            user.save()

            email=request.session["email"]
            useremail = request.session["email"]
            
            try:
                user = Userinfo.objects.get(email=email)
            except:
                return render(request,"login.html",{}) 
            else:
              
                joiningtime = str((user.joining))
                joiningtime = joiningtime[0:11]
                print("joining date : ",joiningtime)

                post = userpost.objects.filter(user_id=user)
                
                user = Userinfo.objects.get(email = useremail)
    
                datass = followers.objects.filter(user_id=user)
                new = []
                new1 = []
                for i in datass:
                    new.append(i.frinds)
                print(new)
                for x in new:
                    myfriends = Userinfo.objects.get(id = x)
                    print(str(myfriends))
                    new1.append(myfriends)
                print(new1)
                size = len(new1)

                suggetion_for_you = []
                
                alluser = Userinfo.objects.all()
                print("All user:-",alluser)
                for i in alluser:
                    print(i.email)
                    print(i)
                    if(str(i.email) == useremail) or (i in new1):
                        print("********")
                        continue
                    else:
                        suggetion_for_you.append(i)
                return render(request,"User/home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":suggetion_for_you,"size":size})
        else:
            user.save()
            email=request.session["email"]
            useremail = request.session["email"]
            
            try:
                user = Userinfo.objects.get(email=email)
            except:
                return render(request,"User/login.html",{}) 
            else:
              
                joiningtime = str((user.joining))
                joiningtime = joiningtime[0:11]
                print("joining date : ",joiningtime)

                post = userpost.objects.filter(user_id=user)
                
                user = Userinfo.objects.get(email = useremail)
    
                datass = followers.objects.filter(user_id=user)
                new = []
                new1 = []
                for i in datass:
                    new.append(i.frinds)
                print(new)
                for x in new:
                    myfriends = Userinfo.objects.get(id = x)
                    print(str(myfriends))
                    new1.append(myfriends)
                print(new1)
                size = len(new1)

                suggetion_for_you = []
                
                alluser = Userinfo.objects.all()
                print("All user:-",alluser)
                for i in alluser:
                    print(i.email)
                    print(i)
                    if(str(i.email) == useremail) or (i in new1):
                        print("********")
                        continue
                    else:
                        suggetion_for_you.append(i)
                return render(request,"User/home.html",{"user":user,"joiningtime":joiningtime,"datas":post,"all":suggetion_for_you,"size":size})
        
        


   
