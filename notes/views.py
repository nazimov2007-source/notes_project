from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Note

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Category, Note


def index(request):
    # 1. Оптимизация: JOIN для category и owner, отдельный запрос для tags
    notes = Note.objects.select_related("category", "owner").prefetch_related("tags")

    # Фильтры
    if request.GET.get("category"):
        notes = notes.filter(category_id=request.GET["category"])
    if request.GET.get("active"):
        notes = notes.filter(is_done=False)
    if request.GET.get("q"):
        notes = notes.filter(title__icontains=request.GET["q"])

    # 2. Считаем количество на стороне базы (SELECT COUNT(*))
    total = notes.count()

    # 3. Ограничиваем выборку 300 записями (LIMIT 300)
    notes = notes[:300]

    # 4. Считаем заметки для категорий одним запросом (GROUP BY)
    categories = Category.objects.annotate(notes_count=Count("notes")).order_by("name")

    return render(request, "notes/note_list.html", {
        "notes": notes, "total": total, "categories": categories,
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