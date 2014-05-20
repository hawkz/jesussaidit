from django.db import models


class Chapter(models.Model):
    BOOK = (
        (40, 'Matthew'),
        (41, 'Mark'),
        (42, 'Luke'),
        (43, 'John'),
        (44, 'Acts'),
        (46, '1 Corinthians'),
        (47, '2 Corinthians'),
        (54, '1 Timothy'),
        (66, 'Revelation'),
    )
    book = models.IntegerField(max_length=2, choices=BOOK)
    chapter = models.IntegerField(max_length=3)
    content = models.TextField()

    def __unicode__(self):
        return "{book} - {chapter}".format(book=self.book, chapter=self.chapter)

    class Meta:
        unique_together = ('book', 'chapter')
        ordering = ['book', 'chapter']

    def next(self):
        try:
            return Chapter.objects.filter(id__gt=self.id).order_by('book')[0]
        except IndexError:
            return None

    def prev(self):
        try:
            return Chapter.objects.filter(id__lt=self.id).order_by('-book')[0]
        except IndexError:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('chapter-view', (), {'pk': self.id})


class Quote(models.Model):
    quote = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    chapter = models.ForeignKey(Chapter)
    verse = models.IntegerField(max_length=3)
    endverse = models.IntegerField(max_length=3)

    def __unicode__(self):
        return self.slug

    class Meta:
        unique_together = ('chapter', 'verse')
        ordering = ['chapter', 'verse']

    def next(self):
        try:
            return Quote.objects.filter(id__gt=self.id).order_by('id')[0]
        except IndexError:
            return None

    def prev(self):
        try:
            return Quote.objects.filter(id__lt=self.id).order_by('-id')[0]
        except IndexError:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('quote-view', (), {'slug': self.slug})
