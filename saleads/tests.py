from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import SaleAd
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import tempfile
import shutil

class SaleAdTestCase(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')

        self.storage = FileSystemStorage(location=self.temp_dir)
        self.client = Client()

    def test_image_upload_view(self):
        url = reverse('sale_ad_view')  
        
        response = self.client.post(url, {'image': self.image, 'details': 'Test Image Details'}, format='multipart')

        self.assertEqual(response.status_code, 200)
        
        self.assertIn('uploaded_file_url', response.context)
        self.assertIn('description', response.context)

        self.assertTrue(SaleAd.objects.exists())

    def test_sale_ad_creation(self):
        SaleAd.objects.create(title='Test Ad', image='path/to/image.jpg', description='Test Description')

        sale_ad = SaleAd.objects.get(title='Test Ad')

        self.assertEqual(sale_ad.description, 'Test Description')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

