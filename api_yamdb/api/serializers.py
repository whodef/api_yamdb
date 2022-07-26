import uuid

from django.core.mail import send_mail
from pkg_resources import require
from rest_framework import exceptions, filters, serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from categories.models import Category, Genre, Title
from reviews.models import Comment, Review


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=('username', 'email')
            )
        ]

    @staticmethod
    def validate_username(value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value

    def create(self, validated_data):
        confirmation_code = str(uuid.uuid4())
        confirmation_message = (
            'Здравствуйте! Спасибо за регистрацию в проекте YaMDb. ',
            f'Ваш код подтверждения: {confirmation_code}. ',
            'Он понадобится для получения токена для работы с Api YaMDb.',
        )
        email = validated_data['email']
        username = validated_data['username']

        send_mail(
            'Код подтверждения регистрации',
            f'{confirmation_message}',
            'from@example.com',
            [email],
        )

        user = User.objects.create(
            username=username, email=email, confirmation_code=confirmation_code
        )
        return user


class GetTokenSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'confirmation_code', 'token')

    def validate(self, data):
        existing = User.objects.filter(
            username=data['username'],
        ).exists()

        if not existing:
            raise exceptions.NotFound('Пользователь не найден')

        user = User.objects.get(username=data['username'])

        if not user.confirmation_code == data['confirmation_code']:
            raise exceptions.ParseError('Код подтверждения не верный')
        return data

    @staticmethod
    def get_token(obj):
        username = list(obj.items())[0][1]
        confirmation_code = list(obj.items())[1][1]
        user = User.objects.get(
            username=username, confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def get_id(obj):
        username = list(obj.items())[0][1]
        user = User.objects.get(username=username)
        return user.id


class AdminUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=['username', 'email']
            )
        ]
        filter_backends = (filters.SearchFilter,)
        search_fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = (
            'role',
            'username',
            'email',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )
    title = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        # print(dir(self.context['view'].kwargs))
        # print(self.context['view'].kwargs['title_id'])
        return self.context['view'].kwargs['title_id']

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'rating',
            'pub_date',
            'title'
        )
        # read_only_fields = ('title',)
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
            ),
        )

    # def create(self, validated_data):
        # print(dir(self.context['request']))
        # print(self.context['request'].data['title'])
        # validated_data['title'] = self.context['request'].data['title']
        # return super().create(validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        genre_list = []
        for genre_data in data['genre']:
            genre = GenreSerializer(Genre.objects.get(slug=genre_data)).data
            genre_list.append(genre)
        data['genre'] = genre_list
        data['category'] = CategorySerializer(
            Category.objects.get(slug=data['category'])
        ).data
        return data
