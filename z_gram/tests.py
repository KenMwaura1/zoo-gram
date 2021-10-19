from django.test import TestCase
from .models import UserProfile, UserPost
from django.contrib.auth.models import User


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='zoo-test')
        self.user.save()

        self.profile_test = UserProfile(id=13, username='image', profile_picture='default.jpg',
                                        bio='this is a test profile',
                                        user=self.user)

    def tearDown(self):
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.profile_test, UserProfile))

    def test_save_profile(self):
        self.profile_test.save_profile()
        after = UserProfile.objects.all()
        self.assertTrue(len(after) > 0)

