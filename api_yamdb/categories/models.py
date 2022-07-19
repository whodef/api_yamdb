from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название жанра')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=48, verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='title'
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.DO_NOTHING)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.genre} {self.title}'
