from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save

from datetime import date

from transliterate import translit


def pre_save_slug(sender, instance, *args, **kwargs):
    """
    Функция-генератор слага на основе названия.
    Использует сигнал presave к базе данных.
    Пытается создать слаг-транслит русского названия, иначе делать слаг из английского.
    Обязательные требования: у модели должны быть поля title и slug.
    Примеры: Терминатор(id:1) -> 1-terminator
    Terminator 2(id:2) -> 2-terminator-2
    """
    if not instance.slug:
        try:
            instance.slug = f"{instance.pk}-{slugify(translit(instance.title, reversed=True))}"
        except:
            instance.slug = f"{instance.pk}-{slugify(instance.title)}"


class Person(models.Model):
    """Актеры и режиссеры"""
    first_name = models.CharField("Имя", max_length=90)
    last_name = models.CharField("Фамилия", max_length=90)
    second_name = models.CharField("Отчество", max_length=90, blank=True)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def get_full_name(self):
        full_name = f"{self.first_name} {self.second_name} {self.last_name}" if self.second_name else \
            f"{self.first_name} {self.last_name}"
        return full_name

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Жанр", max_length=60)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField("Название", max_length=120)
    tagline = models.CharField("Слоган", max_length=120, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=90)
    directors = models.ManyToManyField(Person, verbose_name="режиссеры", related_name="film_director")
    actors = models.ManyToManyField(Person, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premier = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fees_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    draft = models.BooleanField("Черновик", default=False)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})

    def get_reviews(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


pre_save.connect(pre_save_slug, sender=Movie)


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=120)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStars(models.Model):
    """Звезды рейтинга"""
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=90)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")
    star = models.ForeignKey(RatingStars, on_delete=models.CASCADE, verbose_name="звезда")

    def __str__(self):
        return f"{self.movie} - {self.star}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=90)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        "self", verbose_name="Родитель", on_delete=models.SET_NULL, null=True, blank=True
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} - {self.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
