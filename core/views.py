from django.shortcuts import render
from django.contrib import messages
from .forms import ContatoForm, ProdutoModelForm
from .models import Produto
from django.shortcuts import redirect


def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.send_email()
            messages.success(request, 'Enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar mensagem')

    context = {
        'form': form
    }

    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            # Pegar os métodos no post, e pegar os arquivos (Imagens nesse caso)
            if form.is_valid():
                form.save()

                messages.success(request, 'Produto salvo com sucesso.')
                form = ProdutoModelForm()
            else:
                messages.error('Erro ao cadastrar produto, tente novamente')
        else:
            form = ProdutoModelForm()

        context = {
            'form': form
        }
        return render(request, 'produto.html', context)
    return redirect('index')
