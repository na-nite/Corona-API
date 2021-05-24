from django.conf.urls.static import static
from django.urls import path
from api_content.views import (
    PostCreate,
    PostList,
    PostRetrieveUpdate,
    PostDelete,
    PostAccept,
    PostReject,
    UserPost,

    PostStatusUpdate,

    ListComments, ListReplies, ListReply, CommentDelete, CreateComment, CreateReply, CommentUpdate, PostListId)
from api_content.views import WriterPostStatusUpdate, WriterPostList, WriterPostRetrieveUpdate, WriterPostCreate, \
    WriterPostDelete, WriterPostAccept, WriterPostReject, WriterPosts

urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>', PostListId.as_view(), name='post-list-id'),

    path('posts/user/', UserPost.as_view(), name='post-user'),
    path('post/update/<int:pk>', PostRetrieveUpdate.as_view(), name='post-update'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/delete/<int:pk>', PostDelete.as_view(), name='post-delete'),
    path('post/moderator/accept/<int:pk>', PostAccept.as_view(), name='post-accept'),
    path('post/moderator/reject/<int:pk>', PostReject.as_view(), name='post-reject'),
    path('post/moderator/status/<int:pk>', PostStatusUpdate.as_view(), name='post-status'),



    path('comment/create/', CreateComment.as_view(), name='comment-create'),
    path('comment/reply/create/', CreateReply.as_view(), name='reply-create'),




    path('comment/child/<int:parent>', ListReplies.as_view(), name='replies-comments'),
    path('comment/reply/<int:pk>', ListReply.as_view(), name='update-replies'),
    path('comment/', ListComments.as_view(), name='comments'),
    path('comment/delete/<int:pk>', CommentDelete.as_view(), name='delete-comment'),
    path('comment/update/<int:pk>', CommentUpdate.as_view(), name='comment-update'),

    path('writer-posts/', WriterPostList.as_view(), name='writer-post-list'),
    path('writer-posts/writer/', WriterPosts.as_view(), name='writer-post'),
    path('writer-post/update/<int:pk>', WriterPostRetrieveUpdate.as_view(), name='writer-post-update'),
    path('writer-post/create/', WriterPostCreate.as_view(), name='writer-post-create'),
    path('writer-post/delete/<int:pk>', WriterPostDelete.as_view(), name='writer-post-delete'),
    path('writer-post/moderator/accept/<int:pk>', WriterPostAccept.as_view(), name='writer-post-accept'),
    path('writer-post/moderator/reject/<int:pk>', WriterPostReject.as_view(), name='writer-post-reject'),
    path('writer-post/moderator/status/<int:pk>', WriterPostStatusUpdate.as_view(), name='writer-post-status'),

]
