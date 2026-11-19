from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Note

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Category, Note

def index(request):
    # 1. Оптимизация ORM
    notes = Note.objects.select_related("category", "owner").prefetch_related("tags")

    # Фильтры
    if request.GET.get("category"):
        notes = notes.filter(category_id=request.GET["category"])
    if request.GET.get("active"):
        notes = notes.filter(is_done=False)
    if request.GET.get("q"):
        notes = notes.filter(title__icontains=request.GET["q"])

    # 2. Считаем общее количество
    total = notes.count()

    # 3. Пагинация (Шаг 5)
    paginator = Paginator(notes, 20)  # 20 заметок на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 4. Кэширование категорий (Шаг 6)
    categories = cache.get("categories_list")
    if not categories:
        categories = Category.objects.annotate(notes_count=Count("notes")).order_by("name")
        cache.set("categories_list", categories, timeout=60 * 15)  # 15 минут

    return render(request, "notes/note_list.html", {
        "page_obj": page_obj, "total": total, "categories": categories,
    })

def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("notes:index")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form, "title": "Новая заметка"})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes:index")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form, "title": "Редактирование"})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("notes:index")
    return render(request, "notes/note_confirm_delete.html", {"note": note})