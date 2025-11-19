from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from user.models import Company
from .models import Review, ReviewReport
from .forms import ReviewForm, ReviewReportForm

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
    
    # Buscar todas as avaliações da empresa
    reviews = Review.objects.filter(company=company)
    
    context = {
        'company': company,
        'reviews': reviews,
        'form': form,
        'user_review': user_review
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


@login_required
def report_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    # Verificar se o usuário já denunciou este review
    existing_report = ReviewReport.objects.filter(review=review, reporter=request.user).first()
    if existing_report:
        messages.warning(request, 'Você já denunciou esta avaliação anteriormente.')
        return redirect('companies:detail', user_id=review.company.user_id)
    
    # Não permitir que o autor do review se denuncie
    if review.client == request.user:
        messages.error(request, 'Você não pode denunciar sua própria avaliação.')
        return redirect('companies:detail', user_id=review.company.user_id)
    
    if request.method == 'POST':
        form = ReviewReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.review = review
            report.reporter = request.user
            report.save()
            messages.success(request, 'Denúncia enviada com sucesso! Nossa equipe irá analisar.')
            return redirect('companies:detail', user_id=review.company.user_id)
    else:
        form = ReviewReportForm()
    
    context = {
        'review': review,
        'form': form,
        'company': review.company
    }
    return render(request, 'companies/report_review.html', context)
