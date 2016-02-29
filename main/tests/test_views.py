from django.test import TestCase, Client
from django.contrib.auth.admin import User
from django.core.urlresolvers import reverse
from sample_image import TEST_IMAGE
from PIL import Image
import os
from path import path
import time
from datetime import datetime
from main.forms import UploadFileForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from StringIO import StringIO
from main.models import UploadFile
from images.settings import BASE_DIR, MEDIA_ROOT
from main.sweep import housekeeping
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

    def test_0_file_image_upload(self):
        """Test if form loads file and can validate only images are loaded."""
        image = InMemoryUploadedFile(
            StringIO(TEST_IMAGE),
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        self.client.login(username=self.admin.username, password=self.password)
        form = UploadFileForm(files={'file': image})
        self.assertEqual(form.is_valid(), True)
        response = self.client.post(reverse("main:home"), {'file': image})
        self.assertRedirects(response, reverse("main:home"))
        files = UploadFile.objects.all()
        self.assertEqual(files.count(), 1)
        self.file_path = "{}{}".format(BASE_DIR, files.first().file.url)
        self.assertTrue(os.path.isfile(self.file_path))

    def test_1_invald_image_upload(self):
        """Test if form loads file and can validate only images are loaded."""
        self.client.login(username=self.admin.username, password=self.password)
        image = TEST_IMAGE
        response = self.client.post(reverse("main:home"), {'file': image})
        self.assertEqual(response.status_code, 403)

    def test_2_effect_on_file(self):
        """Test effects are applied on image."""
        self.test_0_file_image_upload()
        file = UploadFile.objects.first()

        data = {
            "effect": "invert",
            "path": file.file.url
        }

        response = self.client.get(reverse("main:image"), data)
        self.assertTrue(os.path.isfile(BASE_DIR + response.content))

    def test_save_processed_image(self):
        """Test saving of processed image."""
        self.test_0_file_image_upload()
        file = UploadFile.objects.first()
        data = {
            "effect": "invert",
            "path": file.file.url
        }
        response = self.client.get(reverse("main:image"), data)
        data = {
            "effect": "invert",
            "path": response.content
        }
        response = self.client.post(reverse("main:save_effects"), data)
        self.assertRedirects(response, reverse('main:home'))

    def test_get_effects(self):
        """Test if effects are passed ."""
        response = self.client.get(reverse("main:effects"))
        self.assertEqual(response.status_code, 200)

    def test_image_delete(self):
        """Test Deletion of image from system"""
        self.test_0_file_image_upload()
        files = UploadFile.objects.all()
        for file in files:
            response = self.client.get(reverse("main:delete", args=[file.id, ]))
            self.assertEqual(response.content, "1{u'main.UploadFile': 1}")

    def tearDown(self):
        today = datetime.now()
        today_path = today.strftime("%Y/%m/%d")
        # create relative
        media_path = os.path.join('profile', today_path)
        # create media path to get file
        new_path = os.path.join(MEDIA_ROOT, media_path)
        removed = 0
        dir = path(new_path)
        # Replace DIRECTORY with your required directory
        time_in_secs = time.time() - (0)
        for i in dir.walk():
            if i.isfile():
                if i.mtime <= time_in_secs:
                    i.remove()
                    removed +=1


