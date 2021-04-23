from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from questions.models import Question
from trails.models import Trail
from userprofiles.models import Profile
from questions.forms import AnswerForm
from datetime import datetime,timedelta
import time
import pytz

#--------------Globals-------------------#
IST = pytz.timezone('Asia/Kolkata')
starttime = IST.localize(datetime(2021,4,22,19,0,0,0))
endtime =   IST.localize(datetime(2021,4,23,19,0,0,0))
#----------------------------------------#



@login_required
def nextQuestion(request):
    if datetime.now(tz=IST) < starttime:
        return redirect(reverse_lazy('prestart'))
    elif datetime.now(tz=IST) > endtime:
        return redirect(reverse_lazy('conclude'))

        
    profile = request.user.profile
    if checkwinner(profile):
        return render(request,'winner.html',{})

    ques_obj = Question.objects.get(identifier=profile.curr_ques_id)
    data = {
        'question': ques_obj.ques,
        'asset' : ques_obj.asset,
        'ans_input' : AnswerForm(),
        'choosing' : profile.choosing_trail,
    }
    return render(request,'trails.html',context=data)


@login_required
def chooseTrail(request):
    profile = request.user.profile
    if request.is_ajax() and request.method == 'POST':
        trail = request.POST.get('trail')
        if trail in ["A","B","C"]:
            question_filter = trail.lower() + str(profile.attempted_count)
            selected_question = Question.objects.filter(identifier=question_filter)
            profile.curr_ques_id = question_filter
            profile.choosing_trail = False
            profile.save()
            return JsonResponse({'success':True})
    return JsonResponse({'success':False})


@login_required
def checkAnswer(request):
    profile = request.user.profile
    if request.is_ajax() and request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user_ans = form.cleaned_data.get('answer')
            ori_ans = Question.objects.get(identifier=profile.curr_ques_id).ans
            if user_ans.lower() == ori_ans.lower():
                profile.attempted_count+=1
                profile.score+=10
                profile.time_details+='<'+str(datetime.now(tz=IST).isoformat())+','+str(profile.curr_ques_id)+'>'
                profile.choosing_trail = True
                profile.save()

                data = {'correct':True,'winner':checkwinner(profile)}
            else:
                data = {'correct':False,'winner':checkwinner(profile)}
            return JsonResponse(data)        
    else:
        return redirect(reverse_lazy('nextques'))


@login_required
def checkwinner(profile):
    if profile.attempted_count == profile.to_attempt:
        return True
    else:
        return False



def leaderboardView(request):
    profiles = Profile.objects.filter(user__is_staff=False)
    leaderboard_data = []
    for profile in profiles:
        leaderboard_data.append({'user':profile.user.username,'score':profile.score})
    data = {'profiles':leaderboard_data}
    return render(request,'leaderboard.html',data)