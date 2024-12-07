from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from .models import Publication, Article
from category.models import Category
from comment.models import Comment
from comment.forms import CommentForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.get_object()
        context['comments'] = Comment.objects.filter(publication=publication)
        context['form'] = CommentForm()
        return context


class AddCommentView(FormView):
    form_class = CommentForm
    template_name = 'add_comment.html'  # Укажите ваш шаблон для добавления комментария

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Publication, id=kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.publication = self.publication
        comment.author = self.request.user
        comment.save()
        return redirect('publication_detail', pk=self.publication.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication'] = self.publication
        return context