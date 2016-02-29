from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from allauth.socialaccount.providers.facebook.provider import GRAPH_API_URL
from allauth.socialaccount.models import SocialApp


class IndexTestCase(TestCase):
    """Testcase for the Index View."""

    def setUp(self):
        """Create dummmy user info and intialise CLient."""
        self.client = Client()
        self.user_credentials = {
            'id': '90007770022',
            'first_name': 'police',
            'last_name': 'man',
            'email': 'myemail@email.com',

        }
        # initialise Social app
        self.social_app = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id='00090009',
            secret='923298137293829',
        )
        # Add Current site to social app
        self.site = Site.objects.get_current()
        self.social_app.sites.add(self.site)
        self.graph_api_url = GRAPH_API_URL + '/me'

    def test_landing_page_view(self):
        """Test the site is reachable and rendering active."""
        response = self.client.get(reverse('main:home'))
        # response should redirect to login
        self.assertRedirects(response, "/accounts/login/?next=/")
        response = self.client.get(response.url)
        # check if login is page is functional
        self.assertIn('Login with Facebook', response.content)

    def test_login_user(self):
        """Test redirect to dashboard for an already authenticated user."""
        self.client.post(reverse("account_login"), self.user_credentials)
        response = self.client.get(reverse("main:home"))
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_authenticate_new_facebook_user(self):
        """Test new user can successfully authenticates with Facebook."""
        response = self.client.post(
            reverse("account_login"),
            {
                'id': '24141900',
                'first_name': 'mwaleh',
                'last_name': 'lexx',
                'email': 'mwaleh@email.com',
                'photo': 'http://graph.facebook.com/sample_image',
                'picture': {
                    'data': {
                        'url': 'http://graph.facebook.com/sample_image',
                        'is_silouhette': False,
                    }
                }
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('logout', response.content)

    def test_existing_user_can_authenticate_with_facebook(self):
        """Test existing user authenticate with Facebook."""
        response = self.client.post(
            reverse("account_login"),
            {
                'id': '90007770022',
                'first_name': 'police',
                'last_name': 'man',
                'email': 'myemail@email.com',
                'photo': 'http://graph.facebook.com/sample_image',
                'picture': {
                    'data': {
                        'url': 'http://graph.facebook.com/sample_image',
                        'is_silouhette': True,
                    }
                }
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('logout', response.content)

    def test_invalid_facebook_login(self):
        """Test unauthorised login is returned user to login."""
        response = self.client.post(
            reverse("account_login"),
            {
                'first_name': 'police',
                'last_name': 'man',
                'email': 'myemail@email.com',
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn('login', response.content)

    def test_auth_logout(self):
        """Test  user can logout and redirected to the home."""
        # log a user in:
        self.client.post(
            reverse("account_login"),
            self.user_credentials
        )
        # log user out and check response:
        response = self.client.get(
            reverse("main:logout"),
        )
        self.assertRedirects(response, reverse("account_login"))
