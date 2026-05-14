# python -m venv env
# env\Scripts\activate
# pip install django

# python manage.py makemigrations
# python manage.py migrate
# python -m pip install Pillow (опційно)

from django.db import models
from django.utils.text import slugify

# =========================================================
# HELPERS
# =========================================================

def generate_unique_slug(model, value, slug_field="slug"):
    """
    Генерація унікального slug
    """

    base_slug = slugify(value)

    if not base_slug:
        base_slug = "item"

    slug = base_slug
    counter = 1

    while model.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


# =========================================================
# ARTIST
# =========================================================

class Artist(models.Model):
    """Виконавець"""

    name = models.CharField(
        max_length=255,
        unique=True
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    bio = models.TextField(blank=True)

    country = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.ImageField(
        upload_to='artists/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Виконавець"
        verbose_name_plural = "Виконавці"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = generate_unique_slug(
                Artist,
                self.name
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# GENRE
# =========================================================

class Genre(models.Model):
    """Жанр"""

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = generate_unique_slug(
                Genre,
                self.name
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# ALBUM
# =========================================================

class Album(models.Model):
    """Альбом"""

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='albums'
    )

    release_date = models.DateField(
        blank=True,
        null=True
    )

    cover = models.ImageField(
        upload_to='album_covers/',
        blank=True,
        null=True
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='albums',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-release_date', 'title']
        unique_together = ('title', 'artist')
        verbose_name = "Альбом"
        verbose_name_plural = "Альбоми"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = generate_unique_slug(
                Album,
                self.title
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"


# =========================================================
# TRACK
# =========================================================

class Track(models.Model):
    """Трек"""

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks',
        null=True,
        blank=True
    )

    artists = models.ManyToManyField(
        Artist,
        related_name='tracks'
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='tracks',
        blank=True
    )

    duration = models.PositiveIntegerField(
        help_text="Тривалість у секундах",
        null=True,
        blank=True
    )

    track_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    disc_number = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to='tracks/',
        blank=True,
        null=True,
        help_text="Аудіофайл (mp3, wav тощо)"
    )

    is_explicit = models.BooleanField(
        default=False
    )

    lyrics = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'album',
            'disc_number',
            'track_number',
            'title'
        ]

        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = generate_unique_slug(
                Track,
                self.title
            )

        super().save(*args, **kwargs)

    def __str__(self):

        artists = ", ".join(
            a.name for a in self.artists.all()[:3]
        )

        return f"{self.title} — {artists}"

    def get_duration_display(self):

        if not self.duration:
            return None

        minutes = self.duration // 60
        seconds = self.duration % 60

        return f"{minutes}:{seconds:02d}"