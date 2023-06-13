from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from publications.forms import PublicationForm, CommentForm
from publications.models import Publication

# Create your tests here.
class PublicationsTest(TestCase):


    def test_publication_list_view(self):
        client = Client()
        response = client.get(reverse('publications:publications'))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'publications.html')


class PublicationFormTest(TestCase):
    def setUp(self):
        
        user = User.objects.create(
            username = 'juancho',
            first_name = 'Juan',
            last_name = 'Cho',
            email = 'juancho@test.com',
            password = '1234pepe'
        )
        user.set_password(user.password)
        user.save()

        self.user = user



        

    def test_publication_form(self):
        form = PublicationForm(data={
            'title': 'Test Publication',
            'text': 'This is the text of the publication'
        })
        self.assertEqual(True, form.is_valid())
        form.save()

        pub = Publication.objects.filter(title='Test Publication').first()
        self.assertEqual('Test Publication', pub.title)


# Url Tests
class PublicationsUrlsTest(TestCase):
    def test_publications_url(self):
        url = reverse('publications:publications')
        self.assertEqual(url, '/publications/')


    def test_publication_create_url(self):
        url = reverse('publications:publication_create')
        self.assertEqual(url, '/publications/create/')

    def test_publication_create_url(self):
        url = reverse('publications:publication_detail',kwargs={'pk':2})
        self.assertEqual(url, '/publications/2/')


    def test_publication_edit_url(self):
        url = reverse('publications:publication_update', kwargs={'pk': 2})
        self.assertEqual(url, '/publications/2/edit/')


    def test_publication_delete_url(self):
        url = reverse('publications:publication_delete', kwargs={'pk': 2})
        self.assertEqual(url, '/publications/2/delete/')

    def test_pub_comment_create_url(self):
        url = reverse('publications:comment_create',  kwargs={'pubId':2})
        self.assertEqual(url, '/publications/2/comment-create/')

    def test_pub_comment_delete_url(self):
        url = reverse('publications:comment_delete', kwargs={'Id':4})
        self.assertEqual(url, '/publications/4/comment-delete/')
