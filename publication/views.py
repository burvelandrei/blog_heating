from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Publication, Article
from category.models import Category


class PublicationListView(ListView):
    model = Publication
    template_name = 'publication/index.html'
    context_object_name = 'publications'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(article__category_id=category_id) | queryset.filter(video__category_id=category_id)
        return queryset.order_by(self.get_ordering())

    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'title')  
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publication/publication_detail.html'
    context_object_name = 'publication'