from django.db import models
from django.utils.text import slugify


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
    slug = models.SlugField(max_length=20, editable=False)
    chapter = models.IntegerField(max_length=3)
    content = models.TextField()

    def __unicode__(self):
        return "{book} Chapter {chapter}".format(book=self.get_book_display(), chapter=self.chapter)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_book_display())
        super(Chapter, self).save(*args, **kwargs)

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
        return ('chapter-view', (), {'book': self.slug.strip(),
                                     'chapter': unicode(self.chapter)})


class Quote(models.Model):
    quote = models.TextField()
    chapter = models.ForeignKey(Chapter)
    verse = models.IntegerField(max_length=3)
    endverse = models.IntegerField(max_length=3)

    def __unicode__(self):
        return "{book} Chapter {chapter} v{verse}".format(book=self.chapter.get_book_display(),
                                                     chapter=self.chapter.chapter,
                                                     verse=self.verse)

    class Meta:
        unique_together = ('chapter', 'verse')
        ordering = ['chapter', 'verse']

    def next(self):
        try:
            return Quote.objects.filter(id__gt=self.id).select_related().defer("chapter__content").order_by('id')[0]
        except IndexError:
            return None

    def prev(self):
        try:
            return Quote.objects.filter(id__lt=self.id).select_related().defer("chapter__content").order_by('-id')[0]
        except IndexError:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('quote-view', (), {'book': self.chapter.slug.strip(),
                                   'chapter': unicode(self.chapter.chapter),
                                   'verse': unicode(self.verse)})
