from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from .models import Publication
from category.models import Category
from comment.models import Comment
from comment.forms import CommentForm
from tag.models import Tag


class PublicationListView(ListView):
    model = Publication
    template_name = "publication/index.html"
    context_object_name = "publications"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(
                article__category_id=category_id
            ) | queryset.filter(video__category_id=category_id)
        return queryset.order_by(self.get_ordering())

    def get_ordering(self):
        ordering = self.request.GET.get("sort", "title")
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "publication/publication_detail.html"
    context_object_name = "publication"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.get_object()
        context["comments"] = Comment.objects.filter(publication=publication)
        context["tags"] = publication.content_object.tags.all()
        context["form"] = CommentForm()

        if hasattr(publication.content_object, 'image') and publication.content_object.image:
            context["image"] = publication.content_object.image

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = self.object
            comment.author = request.user
            comment.save()
            return redirect('publication_detail', pk=self.object.id)
        context = self.get_context_data(object=self.object)
        context["form"] = form
        return self.render_to_response(context)
