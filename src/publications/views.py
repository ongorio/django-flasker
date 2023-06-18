from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone

from publications.models import Publication, Comment
from publications.forms import PublicationForm, CommentForm



# Create your views here.
class PublicationsListView(generic.ListView):
    model = Publication
    template_name = 'publications.html'
    context_object_name = 'publications'


    def get_queryset(self):
        publications = self.model.objects.order_by('-pub_date').all()
        return publications


class PublicationCreateView(generic.CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'publication_create.html'


    def get_success_url(self, pk) -> str:
        return reverse('publications:publication_detail', kwargs={'pk': pk})


    def form_valid(self, form: PublicationForm):
        
        publication:Publication = form.save(commit=False)
        publication.author = self.request.user
        publication.pub_date = timezone.now()
        publication.save()

        return redirect(self.get_success_url(publication.pk))


class PublicationEditView(generic.UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'publication_edit.html'

    def get_success_url(self) -> str:
        return reverse('publications:publication_detail', kwargs={'pk': self.kwargs['pk']})
    

class PublicationDeleteView(generic.DeleteView):
    model = Publication
    template_name = 'publication_confirm_delete.html'
    success_url = reverse_lazy('publications:publications')


class PublicationDetailView(generic.DetailView):
    model = Publication
    template_name = 'publication_view.html'


class CommentCreateView(generic.RedirectView):

    def post(self, request, *args, **kwargs):
        
        text = request.POST.get('text')
        pubId = self.kwargs['pubId']
        pub = get_object_or_404(Publication, pk=pubId);

        comment = Comment()
        comment.text = text
        comment.publication = pub
        comment.author = request.user
        comment.pub_date = timezone.now()
        comment.save()

        return redirect(reverse('publications:publication_detail', kwargs={'pk': self.kwargs['pubId']}))


class CommentDeleteView(generic.RedirectView):
    http_method_names = ['post',]
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['Id'])
        comment.delete()        

        return redirect(reverse('publications:publication_detail', kwargs={'pk': comment.publication.pk}))

