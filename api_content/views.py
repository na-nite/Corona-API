from article.models import InternautPost
from api_content.serializers import (InternautePostSerializer,
                                     FullIntenautPostSerializer,
                                     DeletePostSerializer,
                                     InternautePostStatusSerializer, CommentsDetailSerializer, CommentsSerializer,
                                     CommentChildSerializer, DeleteCommentSerializer)
from rest_framework import generics, mixins, exceptions
from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser)
from django_filters.rest_framework import DjangoFilterBackend
from api_content.permissions import (IsOwner, )
from comments.models import Comment

from api_content.serializers import FullWriterPostSerializer, DeleteWriterPostSerializer, WriterPostSerializer, \
    WriterPostStatusSerializer
from article.models import WriterPost
from rest_framework.pagination import LimitOffsetPagination

FILTER_FIELDS = ['status', 'date_posted', 'user']


class PostList(mixins.CreateModelMixin, generics.ListAPIView):
    """
    list all posts
    """
    serializer_class = InternautePostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 2 or self.request.user.is_superuser:
                return FullIntenautPostSerializer
        return InternautePostSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            qs = InternautPost.objects.all().filter(deleted=False)
        else:
            qs = InternautPost.objects.all()
        return qs


class PostListId(generics.RetrieveAPIView):
    """
    list all posts
    """
    lookup_field = 'pk'
    serializer_class = InternautePostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 2 or self.request.user.is_superuser:
                return FullIntenautPostSerializer
        else:
            return InternautePostSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            qs = InternautPost.objects.all().filter(deleted=False)
        else:
            qs = InternautPost.objects.all()
        return qs


class UserPost(generics.ListAPIView):
    serializer_class = InternautePostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'date_posted', ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return InternautPost.objects.filter(user=self.request.user, deleted=False)


class PostCreate(generics.CreateAPIView):
    """
    Create a new post
    """
    serializer_class = InternautePostSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = InternautPost.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role == 1:
            serializer.save(user=self.request.user)
        else:
            raise exceptions.ValidationError("this user is not allowed to create posts")


class PostRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Update post
    """
    queryset = InternautPost.objects.all()
    serializer_class = InternautePostSerializer
    permission_classes = [IsOwner, IsAuthenticated]


class PostDelete(generics.RetrieveUpdateAPIView):
    """
    Set a post as deleted
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeletePostSerializer

    def get_queryset(self):
        if self.request.user.role == 2 or self.request.user.is_superuser:
            return InternautPost.objects.all()
        else:
            return InternautPost.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role == 1 or self.request.user.role == 2 or self.request.user.is_superuser:
            serializer.save(deleted=True)
        else:
            raise exceptions.ValidationError("this user is not allowed to delete posts")


class PostReject(generics.RetrieveUpdateAPIView):
    """
    A moderator reject a post
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FullIntenautPostSerializer
    queryset = InternautPost.objects.all()

    def perform_update(self, serializer):
        if self.request.user.role == 2:
            serializer.save(status='rejected')
        else:
            raise exceptions.ValidationError("this user is not allowed to reject posts")


class PostAccept(generics.RetrieveUpdateAPIView):
    """
    A moderator accept a post
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FullIntenautPostSerializer
    queryset = InternautPost.objects.all().filter(deleted=False)

    def get_querset(self):
        return InternautPost.objects.all()

    def perform_update(self, serializer):
        if self.request.user.role == 2:
            serializer.save(status='accepted')
        else:
            raise exceptions.ValidationError("this user is not allowed to validate posts")


class PostStatusUpdate(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = InternautePostStatusSerializer
    permission_classes = [IsAdminUser]
    queryset = InternautPost.objects.all()


# ---------------------Comments section-----------------------#

class ListComments(generics.ListAPIView):
    serializer_class = CommentsDetailSerializer
    pagination_class = LimitOffsetPagination
    queryset = Comment.objects.filter(parent=None)


class ListReplies(generics.ListAPIView):
    """
    List replies of specific comment
    """
    serializer_class = CommentChildSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        parent = self.kwargs['parent']
        return Comment.objects.filter(parent=parent)


class ListReply(generics.RetrieveAPIView):
    # list all comments && replies
    lookup_field = 'pk'
    pagination_class = LimitOffsetPagination
    serializer_class = CommentChildSerializer
    queryset = Comment.objects.filter()


class CreateComment(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    queryset = Comment.objects.filter()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateReply(generics.ListCreateAPIView):
    serializer_class = CommentChildSerializer
    queryset = Comment.objects.filter()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDelete(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = DeleteCommentSerializer
    queryset = Comment.objects.all()

    def perform_update(self, serializer):
        serializer.save(deleted=True)


class CommentUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CommentsSerializer
    queryset = Comment.objects.all()


# ____________Writer Posts section____________ #

class WriterPostList(generics.ListAPIView):
    serializer_class = WriterPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = FILTER_FIELDS
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 2 or self.request.user.is_superuser:
                return FullWriterPostSerializer
        else:
            return WriterPostSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            qs = WriterPost.objects.all().filter(deleted=False)
        else:
            qs = WriterPost.objects.all()
        return qs


class WriterPosts(generics.ListAPIView):
    """
    show current writer posts
    """
    serializer_class = InternautePostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'date_posted', ]

    def get_queryset(self):
        return WriterPost.objects.filter(user=self.request.user, deleted=False)


class WriterPostCreate(generics.CreateAPIView):
    """
    Create a new post
    """
    serializer_class = WriterPostSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = WriterPost.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role == 3:
            serializer.save(user=self.request.user)
        else:
            raise exceptions.ValidationError("this user is not allowed to create articles")


class WriterPostRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Update post
    """
    queryset = WriterPost.objects.all()
    serializer_class = InternautePostSerializer
    permission_classes = [IsOwner, IsAuthenticated]


class WriterPostDelete(generics.RetrieveUpdateAPIView):
    """
    Set a post as deleted
    """
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = DeleteWriterPostSerializer

    def get_queryset(self):
        return WriterPost.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role == 3 or self.request.user.role == 2 or self.request.user.is_superuser:
            serializer.save(deleted=True)
        else:
            raise exceptions.ValidationError("this user is not allowed to delete posts")


class WriterPostReject(generics.RetrieveUpdateAPIView):
    """
    A moderator reject a post
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FullWriterPostSerializer
    queryset = WriterPost.objects.all()

    def perform_update(self, serializer):
        if self.request.user.role == 2:
            serializer.save(status='rejected')
        else:
            raise exceptions.ValidationError("this user is not allowed to reject posts")


class WriterPostAccept(generics.RetrieveUpdateAPIView):
    """
    A moderator accept a post
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FullWriterPostSerializer
    queryset = WriterPost.objects.all().filter(deleted=False)

    def perform_update(self, serializer):
        if self.request.user.role == 2:
            serializer.save(status='accepted')
        else:
            raise exceptions.ValidationError("this user is not allowed to validate posts")


class WriterPostStatusUpdate(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = WriterPostStatusSerializer
    permission_classes = [IsAdminUser]
    queryset = WriterPost.objects.all()
