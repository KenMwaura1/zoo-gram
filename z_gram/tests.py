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


class TestPost(TestCase):
    def setUp(self):
        self.user = User(username='zoo-codes')
        self.user.save()
        self.profile_test = UserProfile(id=3, username='zoo-test', user=self.user)
        # self.profile_test.save()

        self.image_test = UserPost(image='user.png', caption='default test', user=self.profile_test)

    def tearDown(self):
        UserPost.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.image_test, UserPost))

    def test_save_image(self):
        self.image_test.save()
        images = UserPost.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_image(self):
        self.image_test.save()
        self.image_test.delete()
        after = UserPost.objects.all()
        self.assertTrue(len(after) < 1)
