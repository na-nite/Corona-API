from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from article.models import InternautPost
from comments.models import Comment

from article.models import WriterPost

POST_FIELDS_USER = [
    'pk',
    'title',
    'date_posted',
    'deleted',
    'status',
    'content',
    'user',
    'file']

POST_FIELDS_STAFF = POST_FIELDS_USER + ['reported']

COMMENT_FIELDS = [
    'pk',
    'user',
    'post',
    'content',
    'times',
    'deleted',
]

COMMENT_FIELDS_FULL = COMMENT_FIELDS + ['parent']

COMMENT_FIELDS_DETAILS = COMMENT_FIELDS + ['replies', ]

POST_READ_ONLY_STAFF = ('title','content','date_posted','file','user')
class InternautePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternautPost
        fields = POST_FIELDS_USER
        read_only_fields = ('deleted', 'date_posted', 'status', 'user')


class FullIntenautPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternautPost
        fields = POST_FIELDS_STAFF
        read_only_fields = POST_READ_ONLY_STAFF + ('reported',)


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternautPost
        fields = POST_FIELDS_USER
        read_only_fields = POST_READ_ONLY_STAFF + ('status',)


class InternautePostStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternautPost
        fields = POST_FIELDS_USER
        read_only_fields = POST_READ_ONLY_STAFF + ('deleted',)


# ---------------Comments---------------
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = COMMENT_FIELDS_FULL
        read_only_fields = ('user', 'times', 'deleted', 'parent',)



class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = COMMENT_FIELDS_FULL
        read_only_fields = ('user', 'times', 'post')



class CommentsDetailSerializer(serializers.ModelSerializer):
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = COMMENT_FIELDS_DETAILS
        read_only_fields = ('times', 'user', 'replies')

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None


class DeleteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = COMMENT_FIELDS
        read_only_fields = ('user', 'post', 'content', 'times', 'deleted')


# ____________Writer Posts section____________ #


class WriterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterPost
        fields = POST_FIELDS_USER
        read_only_fields = ('deleted', 'date_posted', 'status', 'user')


class FullWriterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterPost
        fields = POST_FIELDS_STAFF
        read_only_fields = POST_READ_ONLY_STAFF + ('reported',)


class DeleteWriterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterPost
        fields = POST_FIELDS_USER
        read_only_fields = POST_READ_ONLY_STAFF + ('status',)


class WriterPostStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterPost
        fields = POST_FIELDS_USER
        read_only_fields = POST_READ_ONLY_STAFF + ('deleted',)
