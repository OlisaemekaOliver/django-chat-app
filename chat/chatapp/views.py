from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message

@login_required
def home(request):
    conversations = request.user.conversations.all()
    return render(request, "chatapp/home.html", {"conversations": conversations})

@login_required
def chat_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by("timestamp")
    return render(request, "chatapp/chat.html", {
        "conversation": conversation,
        "messages": messages
    })
