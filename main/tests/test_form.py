from django.test import TestCase
from django.contrib.auth.admin import User
from django.test import Client
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from main.forms import UploadFileForm
from sample_image import TEST_IMAGE
from StringIO import StringIO
Image.init()


class FormTestCase(TestCase):
    """Test the form can upload and read an image."""

    def setUp(self):
        """Every test needs a client."""
        self.client = Client()
        self.password = 'mypassword'
        self.admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', self.password)

    def test_login(self):
        """Test  login with normal credentials."""
        response = self.client.get('/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)
        # Check that the rendered context contains 5 customers.
        self.assertEqual(response.get('location'), '/accounts/login/?next=/')
        self.client.login(username=self.admin.username, password=self.password)
        response = self.client.get('/')
        # login success
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        """Test if form loads file and can validate only images are loaded."""
        image = InMemoryUploadedFile(
            StringIO(TEST_IMAGE),
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        form = UploadFileForm(files={'file': image})
        self.assertEqual(form.is_valid(), True)


