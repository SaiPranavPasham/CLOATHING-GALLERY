from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import Outfit, WishlistItem


class AuthenticationViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='demo_user',
            email='demo@example.com',
            password='strong-pass-123',
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_authenticated_user_can_view_dashboard(self):
        self.client.login(username='demo_user', password='strong-pass-123')

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Gallery')

    def test_my_fashion_upload_creates_outfit_for_current_user(self):
        self.client.login(username='demo_user', password='strong-pass-123')
        photo = SimpleUploadedFile(
            'look.gif',
            (
                b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
            ),
            content_type='image/gif',
        )

        response = self.client.post(
            reverse('my_fashion'),
            {
                'title': 'Mocha Night',
                'description': 'A cinematic fashion test upload.',
                'photo': photo,
            },
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Outfit.objects.filter(user=self.user).count(), 1)

    def test_dashboard_only_shows_current_users_photos(self):
        other_user = User.objects.create_user(
            username='second_user',
            email='second@example.com',
            password='strong-pass-456',
        )
        Outfit.objects.create(
            user=self.user,
            title='My Look',
            description='Visible to the logged in user.',
            image=SimpleUploadedFile(
                'mine.gif',
                (
                    b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                    b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                    b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                    b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
                ),
                content_type='image/gif',
            ),
        )
        Outfit.objects.create(
            user=other_user,
            title='Other Look',
            description='Should not be visible.',
            image=SimpleUploadedFile(
                'other.gif',
                (
                    b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                    b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                    b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                    b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
                ),
                content_type='image/gif',
            ),
        )

        self.client.login(username='demo_user', password='strong-pass-123')
        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'My Look')
        self.assertNotContains(response, 'Other Look')

    def test_user_can_delete_only_their_own_outfit(self):
        outfit = Outfit.objects.create(
            user=self.user,
            title='Delete Me',
            description='Should be removed from gallery.',
            image=SimpleUploadedFile(
                'delete.gif',
                (
                    b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                    b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                    b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                    b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
                ),
                content_type='image/gif',
            ),
        )

        self.client.login(username='demo_user', password='strong-pass-123')
        response = self.client.post(reverse('delete_outfit', args=[outfit.id]))

        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Outfit.objects.filter(id=outfit.id).exists())

    def test_user_can_toggle_favorite_from_gallery(self):
        outfit = Outfit.objects.create(
            user=self.user,
            title='Favorite Me',
            description='Should become a favorite.',
            image=SimpleUploadedFile(
                'favorite.gif',
                (
                    b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                    b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                    b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                    b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
                ),
                content_type='image/gif',
            ),
        )

        self.client.login(username='demo_user', password='strong-pass-123')
        response = self.client.post(reverse('toggle_favorite', args=[outfit.id]))

        self.assertRedirects(response, reverse('gallery'))
        outfit.refresh_from_db()
        self.assertTrue(outfit.is_favorite)

    def test_wishlist_item_can_be_created(self):
        self.client.login(username='demo_user', password='strong-pass-123')
        photo = SimpleUploadedFile(
            'wishlist.gif',
            (
                b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
            ),
            content_type='image/gif',
        )

        response = self.client.post(
            reverse('wishlist'),
            {
                'title': 'Leather Boots',
                'product_link': 'https://example.com/boots',
                'notes': 'Save this for later.',
                'photo': photo,
            },
        )

        self.assertRedirects(response, reverse('wishlist'))
        self.assertEqual(WishlistItem.objects.filter(user=self.user).count(), 1)
