from django.test import Client

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
<<<<<<< HEAD
from rest_framework_jwt.settings import api_settings

from article.models import InternautPost

payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # tokens
encode_handler = api_settings.JWT_ENCODE_HANDLER
=======

from article.models import InternautPost


>>>>>>> 1ed9da8ea57eb3e177bf5b43fdb37154e0d26918
# create a user
from django.contrib.auth import get_user_model
from comments.models import Comment

User = get_user_model()


class BlogCommentAPITestCase(APITestCase):
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
            title="corona_title1",
            content="corona_content1",
            user=user_obj1
        )

        comment1 = Comment.objects.create(
            post=blog_post,
            content="comment_content1",
            user=user_obj1
        )

        comment2 = Comment.objects.create(
            post=blog_post,
            content="comment_content2",
            user=user_obj
        )
        comment3 = Comment.objects.create(
            content="comment_content3",
            user=user_obj1,
            parent=comment1

        )
        comment4 = Comment.objects.create(
            content="comment_content4",
            user=user_obj1,
            parent=comment1

        )


    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_single_comment(self):
        comment_count = Comment.objects.count()
        self.assertEqual(comment_count, 4)

    def test_list_comments(self):
        # test get list item
        data = {}
        url = api_reverse("comments")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #    print(response.data)

    def test_create_item(self):
        # test get list item
        url = api_reverse("comment-create")

        self.client = Client()
        self.internaut_user = get_user_model().objects.create_user(
            email='admin@test.com',
            password='test'
        )
        self.client.force_login(self.internaut_user)

        data = {"content": "hello am testing comment creation", "user": self.internaut_user.pk}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)


