from django.shortcuts import render
from django.shortcuts import redirect
from .models import Notification,User,Event,Event_Photos,Resources
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Q, F, Max,Count
from datetime import datetime
import json
import requests
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def Home(request):
    return render(request,'index.html')

def Login(request):
    message=None

    if 'is_logedin' not in request.session and request.method!='POST':
        message="Plese Enter your Email  and password "
        return render(request,'login.html',{'message':message})
    elif  request.method=='POST':
  
        user_email=request.POST.get('User_Email')
        user_password=request.POST.get('User_Password')
        try:
            user_detauls=(User.objects.get(pk=user_email))
            if(user_detauls.user_password==user_password):
                request.session['is_logedin']=True
                request.session['logdin_time']=str(datetime.now())
                request.session['user_email']=user_detauls.user_email
                #request.session['first_name']=user_detauls.user_first_name
                #request.session['last_name']=user_detauls.user_last_name
                request.session['is_admin']=user_detauls.is_admin
                request.session['joindate']=str(user_detauls.user_join_date)               
                return redirect('Home')
            else:
                message="Plese chaeck user id/password again"
        except User.DoesNotExist:
            message="Plese chaeck user id/password again or make sure you are regiterd"           
        
        return render(request,'login.html',{'message':message} )
    
    return redirect("Home")

def Logout(request):
    if 'is_logedin' in request.session: 
        del request.session['is_logedin']    
        request.session.clear()
        return redirect('Home')
    return redirect("Home")

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        dob=request.POST.get('date_of_birth')
        password=request.POST.get('password')
        email=request.POST.get('email')
        ccid=request.POST.get('ccid','')
        cfid=request.POST.get('cfid','')
        check_user=User.objects.filter(pk=email) 
        u1=User(user_first_name=first_name,
                    user_last_name=last_name,
                    user_email=email,
                    user_DOB=dob,
                    user_password=password,
                    user_Codechef_id=ccid,
                    user_Codeforces_id=cfid,
                    is_admin=False,
                    user_join_date=datetime.now())
        if not check_user.exists():
            print("innninini")
            u1.save()
            return redirect('Login')
        else :  return render(request,'register.html',{ 'message':"user alredy exists"})
               
    return render(request,'register.html')

def events_port(request):
    events=Event.objects.all()
    up_coming=events.filter(event_start_date__gt=datetime.now()).order_by("-event_start_date")
    past=events.filter(event_end_date__lt=datetime.now()).order_by("-event_start_date")
    current=events.filter(event_start_date__lt=datetime.now()).filter(event_end_date__gt=datetime.now()).order_by("-event_start_date")
    context={
        "up_coming":up_coming,
        "past":past,
        "current":current
    } 
    return render(request,"event.html",context=context)

def event_details(request,event_id=0):
    print(event_id)
    if request.method=='POST':
        event_title=request.POST.get('event_title')
        event_desc=request.POST.get('event_desc')
        event_start_dt=request.POST.get('event_start_date') 
        event_end_dt=request.POST.get('event_end_date')
        event_link=request.POST.get('registration_link')
        print(event_link)
        event_start_dt=datetime.strptime(event_start_dt,'%Y-%m-%dT%H:%M')
        event_end_dt=datetime.strptime(event_end_dt,'%Y-%m-%dT%H:%M')

        if event_id==0:          
            new_event=Event(event_name=event_title,
                            event_start_date=event_start_dt,
                            event_end_date=event_end_dt,
                            event_details=event_desc,
                            event_registation=event_link)
            new_event.save()
            ev_photo=new_event
        else:

            update_event=Event.objects.get(id=event_id)
            update_event.event_name=event_title
            update_event.event_start_date=event_start_dt
            update_event.event_end_date=event_end_dt
            update_event.event_details=event_desc
            update_event.event_registation=event_link
            ev_photo=update_event
            update_event.save()
            removed_photo=request.POST.get('removed_photo_id')
            if(removed_photo):
                removed_photo=set(removed_photo.split(","))
                for  x in removed_photo:
                    Event_Photos.objects.filter(pk=int(x)).delete()         


        for count, x in enumerate(request.FILES.getlist('event_photo')):
            event_photo=Event_Photos(event_id=ev_photo,event_photo=x)
            event_photo.save()

        return redirect('Events_port')
    elif request.method=='GET'and event_id==0:
         return render(request,'event_details.html')
    else:
        event_det=Event.objects.get(pk=event_id)
        event_ph=Event_Photos.objects.filter(event_id=event_det)

        contex={
            "event_id":event_id,
            "title":event_det.event_name,
            "desc":event_det.event_details,
            "start_dt":event_det.event_start_date,
            "start_dt_formated":datetime.strftime(event_det.event_start_date,'%Y-%m-%dT%H:%M') ,
            "end_dt":event_det.event_end_date,
            "end_dt_formated":datetime.strftime(event_det.event_end_date,'%Y-%m-%dT%H:%M') ,
            "event_imgs":event_ph,
            "event_link":event_det.event_registation,
            "MEDIA_URL":settings.MEDIA_URL
        }
    return render(request,'event_details.html',context=contex)

def delete_event(request,event_id):
    ev=Event.objects.filter(pk=event_id).get()
    Event_Photos.objects.get(ev).delete()
    ev.delete()
    return redirect("Events_port")


def profile(request,user_email="my_profile"):
    print(user_email)
    if request.method=='POST':
        user=User.objects.filter(pk=user_email).get()
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        post=request.POST.get('post')
        dob=request.POST.get('dob')
        ccid=request.POST.get('ccid',None)
        cfid=request.POST.get('cfid',None)            
        user.user_first_name=first_name
        user.user_last_name=last_name
        print(ccid,cfid)
        if(post):user.user_post=post
        if(post=="mentor"):
            user.is_admin=True
        user.user_DOB=datetime.strptime(dob,'%Y-%m-%d')
        try:
            photo=request.FILES['profile_photo']
        except MultiValueDictKeyError:
            photo=None
        if(photo):user.user_profile_photo=photo
        if(ccid):user.user_Codechef_id=ccid
        if(cfid):user.user_Codeforces_id=cfid
        user.save()
        return redirect("Home")
    is_user=None
    if('user_email' in request.session and user_email==request.session['user_email']):is_user=True  
    if user_email=="my_profile": 
        user_email= request.session['user_email']
        is_user=True
    user_details=User.objects.filter(pk=user_email).get()
    context={
        "fname":user_details.user_first_name,
        "lname":user_details.user_last_name,   
        "email":user_details.user_email,
        "dob":user_details.user_DOB,
        "dob_formated":datetime.strftime(user_details.user_DOB,'%Y-%m-%d'),
        "ccid":user_details.user_Codechef_id,
        "cfid":user_details.user_Codeforces_id,
        "profile_photo":user_details.user_profile_photo,
        "MEDIA_URL":settings.MEDIA_URL,
        "is_user":is_user,
        "is_admin":user_details.is_admin,
        "post":user_details.user_post
    }
    print(datetime.strftime(user_details.user_DOB,'%Y-%m-%d'))
    return render(request,'profile.html',context=context)

def resources(request):
    all_resources=Resources.objects.all().order_by("-resource_date_time")
    context={
        "resources":all_resources
    }
    if request.method=='POST':
        all_resources=all_resources.filter( Q(resource_name__contains=request.POST['search'])| Q(resource_content__contains=request.POST['search']) ).order_by("-resource_date_time")
        context={
            "resources":all_resources,
        }   
    return render(request,"resources.html",context=context)



def resource_detail(request,resource_id=0):
    if 'is_logedin' in request.session and request.session['is_admin']==True:        
        if request.method=='POST':
            print(resource_id)
            resource_title=request.POST.get('rname')
            resource_desc=request.POST.get('rdesc')
            resource_link=request.POST.get('rlink')
            if resource_id==0:
                new_resource=Resources(resource_name=resource_title,resource_content=resource_desc,resource_link=resource_link,resource_date_time=datetime.now())
                new_resource.save();
                return redirect("Admin_port")
            else:
                update_resource=Resources.objects.filter(pk=resource_id).get()
                update_resource.resource_name=resource_title
                update_resource.resource_content=resource_desc
                update_resource.resource_link=resource_link
                update_resource.save()
                return redirect("Resources")
        context={} 
        if resource_id!=0:
            rid=Resources.objects.filter(pk=resource_id).get()
            print(rid.id)
            context={"resource":rid}
        else :  context={"resource":{ "id":0}}
        return render(request,"resource_detail.html",context=context)
    return redirect("Resources")

def delete_resource(request,resource_id): 
    Resources.objects.filter(pk=resource_id).delete()
    return redirect("Resources")

def contest_details(request):
    curr_time=datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M')
    cc_users=User.objects.exclude(user_Codechef_id="")
    cf_users=User.objects.exclude(user_Codeforces_id="")
    cc_data=[]
    cf_data=[]
    for u in cc_users:
        x=requests.get("https://competitive-coding-api.herokuapp.com/api/codechef/"+u.user_Codechef_id)
        if(x.status_code==200):
            x=x.json()
            cc_data.append([x['rating'], u.user_email, u.user_first_name, u.user_last_name])
    for u in cf_users:
        x=requests.get("https://codeforces.com/api/user.info?handles="+u.user_Codeforces_id)
        if(x.status_code==200):
            x=x.json()
            if 'rating' in x['result'][0]:
                #print(x['result']['rank'])
                cf_data.append([x['result'][0]['rating'], u.user_email, u.user_first_name, u.user_last_name])
    print(cc_data ,cf_data)
    cc_data.sort(reverse=True)
    cf_data.sort(reverse=True)
    response=requests.get("https://clist.by/api/v1/json/contest/?username=mr_chocha&api_key=9f8aeb6f5f831c44c295c509303000e8e7628f94&start__gte="+curr_time)
    data= json.loads(response.text)
    context={
            "response":data['objects'][:20],
             "ccuser":cc_data,
             "cfuser":cf_data}
    return render(request,"contest_details.html",context=context) 

def about(request):
    mentors=User.objects.filter(user_post="mentor")
    admins=User.objects.filter(is_admin=True).exclude(user_post="mentor")
    context={
        "mentors":mentors,
        "admins":admins,
        "MEDIA_URL":settings.MEDIA_URL,
    }
    print(context)
    return render(request,"about.html",context=context)

def admin_port(request):
    if 'is_logedin' in request.session and request.session['is_admin']==True:
        user_details=User.objects.filter(is_admin=False)
        admin_details=User.objects.filter(is_admin=True)
        context={
            "users":user_details,
            "admins":admin_details,
            "total_events":len(Event.objects.annotate(Count('id'))),
            "total_users":(User.objects.filter(is_admin=False).count()),
            "total_admins":(User.objects.filter(is_admin=True).count()),
            "total_resources":Resources.objects.all().count()
        }
        if request.method=='POST':
            message_topic=request.POST.get('topic')
            message_cont=request.POST.get('notification')
            print(message_cont)
            if message_topic!="" and message_cont!="":
                new_noti=Notification(notofication_topic=message_topic,
                                    notofication_content=message_cont,
                                    notofication_datetime=datetime.now())
                new_noti.save()
                context['message']="Notification added successfully"
                return render(request,'admin_panal.html',context=context)
            else : 
                return render(request,'admin_panal.html',context=context)
        else: return render(request,'admin_panal.html',context=context)
    else:
        return redirect("Home")
        
def add_as_admin(request,user_email):
    new_admin=User.objects.filter(user_email=user_email).get()
    new_admin.is_admin=True
    new_admin.save()
    return redirect("Admin_port")

def remove_admin(request,user_email):
    rem_admin=User.objects.filter(user_email=user_email).get()
    rem_admin.is_admin=False
    rem_admin.save()
    return redirect("Admin_port")

def remove_profile(request,user_email):
    User.objects.filter(user_email=user_email).delete()
    return redirect("Admin_port")

def navbar_restructure(request):
    message={}
    notifications_obj=[]
    if 'is_logedin' in request.session:
        message['messaage']='loged_in'
        message['is_admin']=request.session['is_admin']    
        notifications_obj.append(message)
        noti_final=[]
        join_dt=request.session['joindate'].format(datetime.now())
        notifications=Notification.objects.filter(notofication_datetime__gt=join_dt)
        new_notifications=notifications.exclude(notification_seen=User.objects.get(user_email=request.session['user_email'])).order_by("-notofication_datetime")   
        old_notifications=Notification.objects.filter(notification_seen=User.objects.get(user_email=request.session['user_email'])).order_by("-notofication_datetime")   
        for notification in new_notifications:
            noti={
            'id':notification.id,
            'topic':notification.notofication_topic,
            'content':notification.notofication_content,
            'datetime':str((notification.notofication_datetime).strftime("%a,%d %B,%y %I:%M:%S %p"))
            }
            noti_final.append(noti)
        new_noti_final=noti_final
        noti_final=[]
        for notification in old_notifications:
            noti={
            'id':notification.id,
            'topic':notification.notofication_topic,
            'content':notification.notofication_content,
            'datetime':str((notification.notofication_datetime).strftime("%a,%d %B,%y %I:%M:%S %p"))
            }
            noti_final.append(noti)
        old_noti_final=noti_final
        notifications_obj.append({'New_notifications':new_noti_final,'Old_notifications':old_noti_final});
    else : 
        message['messaage']='not_logedin'
        notifications_obj.append(message)
        
    notifications_obj=json.dumps(notifications_obj)
    return HttpResponse(notifications_obj)


def Close_notification(request):
    if request.is_ajax():
        message_id=request.POST.get('seen_message_id')
        print(message_id)
        message_seen=Notification.objects.get(pk=int(message_id))
        user=User.objects.get(pk=request.session['user_email'])
        message_seen.notification_seen.add(user)
        return render(request,'index.html')


def Delete_notification(request):
    if request.is_ajax():
        message_id=request.POST.get('delete_message_id')
        noti= Notification.objects.get(id=message_id)   
        noti.notification_seen.clear()  
        noti.delete()
        print("deleted") 
        return render(request,'index.html')
