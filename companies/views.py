from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Company
from .models import Review
from .forms import ReviewForm
from django.utils import timezone
from .forms import CompanyResponseForm
from .models import BudgetRequest
from .forms import BudgetRequestForm, BudgetResponseForm, ClientResponseForm

@login_required
def request_budget(request, user_id):
    company = get_object_or_404(Company, user_id=user_id)
    
    # Verificar se é cliente
    if not request.user.is_client:
        messages.error(request, 'Apenas clientes podem solicitar orçamentos.')
        return redirect('companies:detail', user_id=user_id)
    
    if request.method == 'POST':
        form = BudgetRequestForm(request.POST, request.FILES)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.company = company
            budget.client = request.user
            budget.save()
            
            messages.success(request, 'Solicitação de orçamento enviada com sucesso!')
            return redirect('companies:budget_requests')
    else:
        form = BudgetRequestForm()
    
    return render(request, 'companies/request_budget.html', {
        'form': form,
        'company': company
    })

@login_required
def budget_requests(request):
    """Lista de orçamentos do usuário"""
    if request.user.is_client:
        # Cliente vê seus próprios orçamentos
        budgets = BudgetRequest.objects.filter(client=request.user)
        template = 'companies/client_budgets.html'
    else:
        # Empresa vê orçamentos recebidos
        budgets = BudgetRequest.objects.filter(company__user=request.user)
        template = 'companies/company_budgets.html'
    
    return render(request, template, {
        'budgets': budgets
    })

@login_required
def budget_detail(request, pk):
    budget = get_object_or_404(BudgetRequest, pk=pk)
    
    # Verificar permissão
    if request.user != budget.client and request.user != budget.company.user:
        messages.error(request, 'Você não tem permissão para visualizar este orçamento.')
        return redirect('companies:list')
    
    # Form para resposta (apenas para empresa e se pendente)
    response_form = None
    if request.user == budget.company.user and budget.status == 'pending':
        response_form = BudgetResponseForm()
    
    return render(request, 'companies/budget_detail.html', {
        'budget': budget,
        'response_form': response_form
    })

@login_required
def respond_budget(request, pk):
    budget = get_object_or_404(BudgetRequest, pk=pk)
    
    # Verificar permissão
    if not budget.can_respond(request.user):
        messages.error(request, 'Você não tem permissão para responder a este orçamento.')
        return redirect('companies:budget_detail', pk=pk)
    
    if request.method == 'POST':
        form = BudgetResponseForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.response_date = timezone.now()
            
            # Se o prestador enviou um preço, muda status para 'quoted'
            if budget.proposed_price and budget.status == 'pending':
                budget.status = 'quoted'
            
            budget.save()
            
            messages.success(request, 'Resposta enviada com sucesso! Aguardando resposta do cliente.')
            return redirect('companies:budget_detail', pk=pk)
    else:
        form = BudgetResponseForm(instance=budget)
    
    return render(request, 'companies/respond_budget.html', {
        'form': form,
        'budget': budget
    })

    
@login_required
def client_respond_budget(request, pk):
    """View para o cliente aceitar ou recusar o orçamento"""
    budget = get_object_or_404(BudgetRequest, pk=pk)
    
    # Verificar permissão
    if not budget.can_accept_reject(request.user):
        messages.error(request, 'Você não tem permissão para responder a este orçamento.')
        return redirect('companies:budget_detail', pk=pk)
    
    if request.method == 'POST':
        form = ClientResponseForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)
            acceptance = form.cleaned_data['acceptance']
            budget.status = acceptance
            budget.client_response_date = timezone.now()
            budget.save()
            
            if budget.status == 'accepted':
                messages.success(request, 'Orçamento aceito! Entre em contato com o prestador para combinar os detalhes.')
            else:
                messages.success(request, 'Orçamento recusado.')
            
            return redirect('companies:budget_detail', pk=pk)
    else:
        form = ClientResponseForm(instance=budget)
    
    return render(request, 'companies/client_respond_budget.html', {
        'form': form,
        'budget': budget
    })

@login_required
def cancel_budget(request, pk):
    budget = get_object_or_404(BudgetRequest, pk=pk)
    
    if not budget.can_cancel(request.user):
        messages.error(request, 'Você não tem permissão para cancelar este orçamento.')
        return redirect('companies:budget_detail', pk=pk)
    
    if request.method == 'POST':
        budget.status = 'cancelled'
        budget.save()
        messages.success(request, 'Solicitação de orçamento cancelada.')
    
    return redirect('companies:budget_requests')

@login_required
def respond_to_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    # Verificar se o usuário é o dono da empresa
    if not review.can_respond(request.user):
        messages.error(request, 'Você não tem permissão para responder a esta avaliação.')
        return redirect('companies:detail', user_id=review.company.user_id)
    
    if request.method == 'POST':
        form = CompanyResponseForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.response_date = timezone.now()
            review.save()
            messages.success(request, 'Resposta enviada com sucesso!')
            return redirect('companies:detail', user_id=review.company.user_id)
    else:
        form = CompanyResponseForm(instance=review)
    
    return render(request, 'companies/respond_review.html', {
        'form': form,
        'review': review
    })

@login_required
def edit_response(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if not review.can_respond(request.user):
        messages.error(request, 'Você não tem permissão para editar esta resposta.')
        return redirect('companies:detail', user_id=review.company.user_id)
    
    if request.method == 'POST':
        form = CompanyResponseForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Resposta atualizada com sucesso!')
            return redirect('companies:detail', user_id=review.company.user_id)
    else:
        form = CompanyResponseForm(instance=review)
    
    return render(request, 'companies/respond_review.html', {
        'form': form,
        'review': review,
        'editing': True
    })

@login_required
def delete_response(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if not review.can_respond(request.user):
        messages.error(request, 'Você não tem permissão para excluir esta resposta.')
        return redirect('companies:detail', user_id=review.company.user_id)
    
    if request.method == 'POST':
        review.company_response = None
        review.response_date = None
        review.save()
        messages.success(request, 'Resposta excluída com sucesso!')
    
    return redirect('companies:detail', user_id=review.company.user_id)

def detail_company(request, user_id):
    company = get_object_or_404(Company, user_id=user_id)
    
    
    # Verificar se o usuário já avaliou esta empresa
    user_review = None
    if request.user.is_authenticated and request.user.is_client:
        try:
            user_review = Review.objects.get(company=company, client=request.user)
        except Review.DoesNotExist:
            user_review = None
    
    # Processar formulário de avaliação
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_client:
        form = ReviewForm(request.POST)
        if form.is_valid():
            if user_review:
                # Atualizar avaliação existente
                user_review.rating = form.cleaned_data['rating']
                user_review.comment = form.cleaned_data['comment']
                user_review.save()
                messages.success(request, 'Avaliação atualizada com sucesso!')
            else:
                # Criar nova avaliação
                review = form.save(commit=False)
                review.company = company
                review.client = request.user
                review.save()
                messages.success(request, 'Avaliação enviada com sucesso!')
            return redirect('companies:detail', user_id=user_id)
    else:
        if user_review:
            form = ReviewForm(instance=user_review)
        else:
            form = ReviewForm()
    
    reviews = Review.objects.filter(company=company)
    
    # Form para resposta (apenas para dono da empresa)
    response_form = None
    if request.user == company.user:
        response_form = CompanyResponseForm()
    
    context = {
        'company': company,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'response_form': response_form,  # NOVO
    }
    return render(request, 'companies/detail.html', context)

def list_companies(request):
    company_list = Company.objects.all().order_by('-average_rating')
    context = {'company_list': company_list}
    return render(request, 'companies/list.html', context)

def search_companies(request):
    # Get all unique cities and jobs for the filter dropdowns
    cities = Company.objects.values_list('city', flat=True).distinct().order_by('city')
    jobs = Company.objects.values_list('job', flat=True).distinct().order_by('job')
    
    # Start with all companies
    company_list = Company.objects.all()
    
    # Apply filters if they exist in the request
    query = request.GET.get('query', '').strip()
    city = request.GET.get('city', '').strip()
    job = request.GET.get('job', '').strip()
    
    if query:
        company_list = company_list.filter(user__name__icontains=query)
    
    if city:
        company_list = company_list.filter(city__iexact=city)
    
    if job:
        company_list = company_list.filter(job__iexact=job)
    
    # Ordenar por avaliação
    company_list = company_list.order_by('-average_rating')
    
    context = {
        'company_list': company_list,
        'cities': cities,
        'jobs': jobs,
        'search_params': {
            'query': query,
            'city': city,
            'job': job,
        }
    }
    
    return render(request, 'companies/search.html', context)

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, client=request.user)
    user_id = review.company.user_id
    review.delete()
    messages.success(request, 'Avaliação removida com sucesso!')
    return redirect('companies:detail', user_id=user_id)
