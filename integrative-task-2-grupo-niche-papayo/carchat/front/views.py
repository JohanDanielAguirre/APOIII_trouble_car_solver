from collections import defaultdict
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.conf import settings
from selenium.webdriver.common.devtools.v85.tracing import get_categories

from .forms import UserRegisterForm, UserLoginForm
from .models import Usuario, Chat
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = form.cleaned_data["password"]
            usuario.save()
            request.session["usuario_id"] = usuario.id
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    error = None
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                usuario = Usuario.objects.get(email=email, password=password)
                request.session["usuario_id"] = usuario.id  # Guarda la sesión del usuario
                return redirect("home")  # Redirige a la página de chat
            except Usuario.DoesNotExist:
                error = "Correo o contraseña incorrectos"
    else:
        form = UserLoginForm()
        return render(request, "login.html", {"form": form, "error": error})

def log_out(request):
    request.session.flush()
    return redirect("login")

def password_reset_request(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            error = "Las contraseñas no coinciden."
        else:
            try:
                usuario = Usuario.objects.get(email=email)
                usuario.password = new_password  # Actualiza la contraseña
                usuario.save()
                return redirect("login")  # Redirige al login
            except Usuario.DoesNotExist:
                error = "El correo no está registrado."
    return render(request, "forgetPassword.html", {"error": error})

def chat_history(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")
    usuario = Usuario.objects.get(id=usuario_id)
    chats = Chat.objects.filter(user=usuario)
    return render(request, "chat_history.html", {"chats": chats, "usuario": usuario})


def home(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")
    usuario = Usuario.objects.get(id=usuario_id)

    # Load the questions and answers from the JSON file
    with open(settings.BASE_DIR / 'front/static/qans.json', 'r') as file:
        qans_data = json.load(file)

    if request.method == "POST":
        pregunta = request.POST.get("pregunta").strip().lower()
        current_category = request.session.get('current_category')

        if pregunta == "hola":
            response_data = list_categories(qans_data)
        elif not current_category:
            response_data = get_category(pregunta, qans_data, request.session)
        else:
            response_data = get_response(pregunta, qans_data, request.session)

        respuesta = response_data['respuesta']
        next_question = response_data.get('next_question')
        current_category = response_data.get('current_category')

        # Guardar el chat
        chat = Chat.objects.create(user=usuario, question=pregunta, answer=respuesta)
        timestamp = chat.timestamp.strftime("%H:%M %p")

        return JsonResponse({
            'pregunta': pregunta,
            'respuesta': respuesta,
            'timestamp': timestamp,
            'next_question': next_question,
            'current_category': current_category
        })

    # Listar categorías al cargar la página
    response_data = list_categories(qans_data)
    respuesta = response_data['respuesta']

    chats = Chat.objects.filter(user=usuario)
    chats_by_date = defaultdict(list)
    for chat in chats:
        date = chat.timestamp.strftime("%d/%m/%Y")
        chats_by_date[date].append(chat)

    return render(request, "chat.html", {
        "respuesta": respuesta,
        "usuario": usuario,
        "chats_by_date": dict(chats_by_date),
        "current_category": request.session.get('current_category'),
        "current_step": request.session.get('current_step')
    })
def list_categories(qans_data):
    categories = [data['name'] for data in qans_data['categories'].values()]
    return {
        'respuesta': "Por favor, selecciona una categoría de la lista: " + ", ".join(categories),
        'categories': categories
    }

def get_category(pregunta, qans_data, session):
    # Buscar la categoría seleccionada
    for category, data in qans_data['categories'].items():
        if pregunta.lower() == data['name'].lower():
            current_category = category
            session['current_category'] = current_category
            # Tomar la primera pregunta de la categoría
            first_question = data['questions'][0]
            session['current_step'] = 0
            return {
                'respuesta': first_question['question'],
                'current_category': current_category
            }

    # Si no se encuentra la categoría
    return {
        'respuesta': "No tenemos esa categoría. Por favor, selecciona una categoría válida de la lista.",
        'current_category': None
    }

def get_response(pregunta, qans_data, session):
    current_category = session.get('current_category')
    current_step = session.get('current_step')

    category_data = qans_data['categories'][current_category]
    current_question = category_data['questions'][current_step]

    if pregunta.lower() in ['sí', 'si', 'yes']:
        respuesta = current_question['yes_response']
        next_step = current_question.get('next')
        if next_step:
            if isinstance(next_step, dict):
                session['current_step'] += 1
                return {
                    'respuesta': respuesta + " " + next_step['question'],
                    'next_question': next_step['question'],
                    'current_category': current_category
                }
            else:
                return {
                    'respuesta': respuesta + " ¿Deseas cambiar de categoría?",
                    'next_question': "Fin de categoría",
                    'current_category': current_category
                }
        else:
            return {
                'respuesta': respuesta + " ¿Deseas cambiar de categoría?",
                'next_question': "Fin de categoría",
                'current_category': current_category
            }

    elif pregunta.lower() in ['no']:
        if current_question.get('no_response'):
            respuesta = current_question['no_response']
            next_step = current_question.get('next')
            if next_step:
                if isinstance(next_step, dict):
                    session['current_step'] += 1
                    return {
                        'respuesta': respuesta + " " + next_step['question'],
                        'next_question': next_step['question'],
                        'current_category': current_category
                    }
                else:
                    return {
                        'respuesta': respuesta + " ¿Deseas cambiar de categoría?",
                        'next_question': "Fin de categoría",
                        'current_category': current_category
                    }
            else:
                return {
                    'respuesta': respuesta + " ¿Deseas cambiar de categoría?",
                    'next_question': "Fin de categoría",
                    'current_category': current_category
                }
        else:
            return {
                'respuesta': "No entendí tu respuesta. Por favor responde Sí o No.",
                'next_question': current_question['question'],
                'current_category': current_category
            }

    elif pregunta.lower() in ["sí, cambiar categoría", "si, cambiar categoria"]:
        session.pop('current_category', None)
        session.pop('current_step', None)
        return list_categories(qans_data)

    else:
        return ({
            'respuesta': "No entendí tu respuesta. Por favor responde Sí o No.",
            'next_question': current_question['question'],
            'current_category': current_category
        })
@csrf_exempt
def delete_history(request):
    if request.method == 'POST':
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return JsonResponse({'success': False, 'error': 'User no authenticated'})
        usuario = Usuario.objects.get(id=usuario_id)
        Chat.objects.filter(user=usuario).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Forbidden method'})