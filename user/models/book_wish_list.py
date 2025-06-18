from django.db import models
from .user import User
from book.models import Book
from core.models import BaseModel


class BookWishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"

    class Meta:
        verbose_name = "Book Wish List"
        verbose_name_plural = "Book Wish Lists"
