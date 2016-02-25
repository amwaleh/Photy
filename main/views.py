from __future__ import print_function
from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from datetime import datetime
import os
import shutil
from forms import UploadFileForm
from models import UploadFile
from effects import effect
from images.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR
from sweep import housekeeping
import random


class Effects(TemplateView):
    """Return the available effects."""

    def get(self, requests):
        """Return all the effects available."""
        return HttpResponse(content=[effect.keys()])


class Home(LoginRequiredMixin, TemplateView):
    """Create dashboard and save new upload."""

    login_required = True
    template_name = 'main/index.html'

    def post(self, request):
        """Save uploads and thumbnails."""
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(
                file=request.FILES['file'], owner=request.user)
            new_file.save()
            return HttpResponseRedirect(reverse('main:home'))
        return HttpResponse("Error", status=403)

    def get(self, request):
        """Handle dashboard output information."""
        form = UploadFileForm()
        file = UploadFile.objects.filter(owner=request.user)
        data = {'form': form,
                'images': file,
                'effects': effect.keys(),
                }
        return render(request, self.template_name, data)


class SaveProcessedImage(LoginRequiredMixin, TemplateView):
    """Save processed images on demand."""

    login_required = True
    template_name = 'main/index.html'

    def post(self, request):
        """Save processed image."""
        if request.POST.get('path'):
            today = datetime.now()
            today_path = today.strftime("%Y/%m/%d")
            path = request.POST.get('path')
            filename = os.path.basename(path)
            # create relative
            media_path = os.path.join('profile', today_path, filename)
            # create media path to get file
            new_path = os.path.join(MEDIA_ROOT, media_path)
            # check if file has been copied
            path_ready = self.copyfiles(path, new_path)
            if path_ready:
                new_file = UploadFile.objects.all()
                new_file.file = new_path
                new_file.owner = request.user
                new_file.update_or_create(
                    file=media_path, owner=request.user)
                return HttpResponseRedirect(reverse('main:home'))
            return HttpResponse("Error occured", status=405)

    def copyfiles(self, source, destination):
        """Create Folder and files."""
        if not os.path.isdir(os.path.dirname(destination)):
            os.mkdir(os.path.dirname(destination))
        abs_source = "{}{}".format(BASE_DIR, source)
        try:
            shutil.copy(abs_source, destination)
        except:
            return False
        return True


class ImageProcessing(LoginRequiredMixin, TemplateView):
    """Process image and return the route of the processesed image."""

    def get(self, request):
        """Process and temporarily save imag."""
        user_id = request.user.id
        string = request.GET.get('effect')
        path = request.GET.get(r'path')
        add_effect = string.replace(u'\xa0', '')
        file_name = os.path.basename(path)
        file, ext = os.path.splitext(file_name)
        # add random number to image tomake it unique
        rand = random.randint(0, 100)
        image = Image.open("{}{}".format(BASE_DIR, path))
        # create absolute path for folder creation
        output = "{}{}{}{}".format(
            BASE_DIR, MEDIA_URL, 'CACHE/temp/', user_id)
        if not os.path.exists(output):
            os.makedirs(output)
        # set path to save processed image
        temp_file_location = "{}{}.PNG".format(rand, file)
        # set route for exclusive to thumbnails
        if request.GET.get('preview'):
            temp_file_location = "thumbnails/{}.PNG".format(add_effect)
        temp_file = os.path.join(output, temp_file_location)
        if not os.path.isdir(os.path.dirname(temp_file)):
            os.makedirs(os.path.dirname(temp_file))
        final_image = effect[add_effect](image)
        housekeeping(output)
        final_image.save(temp_file, 'PNG')
        file_url = os.path.join(
            MEDIA_URL, 'CACHE', 'temp', str(user_id), temp_file_location)
        return HttpResponse(file_url)


class DeleteImage(LoginRequiredMixin, TemplateView):
    """Deletes Photos and records."""

    def get(self, request, id):
        """Delete record and images."""
        image = UploadFile.objects.get(id=id)
        if image:
            return HttpResponse(image.delete())
        return HttpResponse(image.delete())
