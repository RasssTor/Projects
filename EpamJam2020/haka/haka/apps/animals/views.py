from django.shortcuts import render
from .models import Animal
from django.utils import timezone
from django.shortcuts import redirect
from .forms import ImageUploadForm
import smtplib


# output list of animal's cards
def index(request):
    latest_animals_list = Animal.objects.order_by('-pub_date')
    return render(request, 'animals/main.html', {'latest_animals_list': latest_animals_list})


# POST request for update card's list
def vote(request):
    sex = ""
    if request.POST['class'] == "Собака":
        if request.POST['sex'] == "male":
            sex = "Кабель"
        elif request.POST['sex'] == "female":
            sex = "Сука"  #
        else:  # check sex
            sex = "Неизвестно"  # of animal
    elif request.POST['class'] == "Кот":  #
        if request.POST['sex'] == "male":  #
            sex = "Кот"  #
        elif request.POST['sex'] == "female":
            sex = "Кошка"
        else:
            sex = "Неизвестно"

    # create obj animal
    a = Animal(animal_name=request.POST['name'],
               animal_sex=sex,
               animal_class=request.POST['class'],
               animal_age=int(request.POST['year']) * 12 + int(request.POST['month']),
               pub_date=timezone.now(), vk_url=request.POST['email'])

    # save obj
    a.save(force_insert=True)

    # add animal's photo
    if request.method == 'POST':
        request.FILES['image'].name = str(a.id) + '.jpg'
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Animal.objects.get(pk=a.id)
            m.model_pic = form.cleaned_data['image']
            m.save()

        return redirect('/animals')


# send notification on mail
def send_message(request):
    login = 'exampleMail@gmail.com'
    password = '12345678'
    name = request.POST['name']
    phone = request.POST['phone']
    msg = request.POST['msg']
    num = request.POST['id']

    a = Animal.objects.get(pk=num)
    sender = 'minecraftboyvlad@gmail.com'
    receivers = [a.vk_url]

    #formation of message
    message = "\r\n".join((
        "From: %s" % sender,
        "Subject: %s" % "Подари шанс. На твоего подопечного откликнулись.",
        "",
        "{} откликнулся на ваше объявление({}).\n{}\nТелефон: {}".format(name, a.animal_name, msg, phone)
    )).encode(encoding='UTF-8')

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(login, password)
    smtpObj.sendmail(login, receivers, message)

    return redirect('/animals')
