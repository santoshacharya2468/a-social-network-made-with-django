from .models import *
from django.http import JsonResponse
from django.contrib.auth.models import User


def send_message(request,id):
    if request.method=='POST':
        message=Message()
        message.sender=request.user.id
        message.receiver=id
        message.body=request.POST['message']
        message.save()
        msg_notify=Message_Notification()
        msg_notify.sender=request.user.id
        msg_notify.receiver=id
        msg_notify.save()
        message={'message':message.body,'profile_picture':request.user.profile.profile_picture.url}
        return JsonResponse(message)
    else:
        receiver=User.objects.get(id=id)
        u_id=request.user.id
        new_message = Message.objects.filter(sender=id).filter(receiver=u_id).exclude(Q(del_by_sender = u_id)|Q(del_by_receiver=u_id)).filter(seen=False)[0]
        data={'message':new_message.body,"profile_picture":receiver.profile.profile_picture.url}
        new_message.seen=True
        new_message.save()
        return JsonResponse(data)
