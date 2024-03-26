from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Message

User = get_user_model()


@login_required
def index(request):
    users = User.objects.exclude(username=request.user.username)

    return render(request, 'chat/index.html', {'users': users})


@login_required
def room(request, pk):
    receiver = User.objects.get(pk=pk)
    username_list = [receiver.username, request.user.username]

    message_list = Message.objects.filter(author__username__in=username_list,
                                          to__username__in=username_list).order_by('timestamp')
    template_name = 'chat/partials/message-list.html'
    paginator = Paginator(message_list, 12)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = paginator.num_pages
        template_name = 'chat/room.html'
    messages = paginator.get_page(page_number)

    return render(request, template_name, {'messages': messages, 'receiver': receiver})


@login_required
def search_user(request):
    if request.method == 'POST':
        username = request.POST['username']

        users = User.objects.filter(username__icontains=username).exclude(pk=request.user.pk)

        return render(request, 'chat/partials/user-list.html', {'users': users})
