from django.db import models
from core.models import BaseModel
from user.models import User


class Book(BaseModel):
    
    STATUS = (
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('archived', 'Archived')
    )
    
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    status = models.CharField(max_length=20, choices=STATUS, default='published')
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    cover_image = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_copies = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('Category', related_name='books', blank=True)
    tags = models.ManyToManyField('Tag', related_name='books', blank=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    translator = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True)  # e.g., "5 x 8 inches"
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in grams
    country = models.CharField(max_length=100, blank=True, null=True)  # Country of publication
    is_new = models.BooleanField(default=False, help_text="Indicates if the book is new")
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-published_date']  # Order by published date descending


class BookImage(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.book.title}"

    class Meta:
        verbose_name = "Book Image"
        verbose_name_plural = "Book Images"
        ordering = ['book__title']  # Order by book title


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    index_number = models.PositiveIntegerField(default=0, help_text="Used for ordering categories on the frontend")
    is_featured = models.BooleanField(default=False, help_text="Indicates if the category is featured")
    is_favorite = models.BooleanField(default=False, help_text="Indicates if the category is a favorite")
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

