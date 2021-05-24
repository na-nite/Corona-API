from django.test import Client

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
# create a user
from django.contrib.auth import get_user_model
from article.models import InternautPost

User = get_user_model()


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(email='gn_fekir@esi.dz', role=1)
        user_obj.set_password("nadjet")

        user_obj.save()
        user_obj1 = User(email='gn_kawther@esi.dz', role=1)
        user_obj1.set_password("kawther")
        user_obj1.save()
        blog_post = InternautPost.objects.create(
            title="corona_title",
            content="corona_content",
            user=user_obj1
        )
        blog_post2 = InternautPost.objects.create(
            title="corona_title2",
            content="corona_content2",
            user=user_obj
        )
        blog_post3 = InternautPost.objects.create(
            title="corona_title3",
            content="corona_content3",
            user=user_obj1
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_single_post(self):
        post_count = InternautPost.objects.count()
        self.assertEqual(post_count, 3)

    # posts/
    def test_get_list(self):
        # test get list item
        data = {}
        url = api_reverse("post-list")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    # post/create /
    def test_create_item(self):
        # test creating a post
        data = {"title": "creating test", "content": "hello am testing my api_content"}
        url = api_reverse("post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # post/<int:pk>
    def test_get_item(self):
        # test get a post
        blog_post = InternautPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    # post/update/< int: pk > not authenticated
    #def test_update_item(self):
        # test update a post
    #    blog_post = InternautPost.objects.first()
    #    url = blog_post.get_api_url_update()
    #    data = {"title": "creating testtttttttt", "content": "hello am testing my api_content"}
    #    response = self.client.put(url, data, format='json')
    #    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # print(response.data)

    # post/update/< int: pk > authenticated
    # def test_update_item_with_user(self):
    #     # test update a post
    #
    #     self.client = Client()
    #     self.internaut_user = get_user_model().objects.create_user(
    #         email='admin@test.com',
    #         password='test'
    #     )
    #     self.client.force_login(self.internaut_user)
    #
    #     blog_post = InternautPost.objects.create(
    #         title="corona_title",
    #         content="corona_content",
    #         user=self.internaut_user
    #     )
    #     url = blog_post.get_api_url_update()
    #
    #     data = {"title": "creating testtttttttt", "content": "hello am testing my api_content"}
    #     # user_obj = User.objects.first()
    #     # payload = payload_handler(user_obj)
    #     # token_rsp = encode_handler(payload)
    #     # self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_rsp)
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    #     print(response.data)
