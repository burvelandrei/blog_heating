from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Publication, Article


class PublicationListView(ListView):
    model = Publication
    template_name = 'publication/index.html'
    context_object_name = 'publications'
    paginate_by = 10

    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'title')
        return ordering


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publication/publication_detail.html'
    context_object_name = 'publication'