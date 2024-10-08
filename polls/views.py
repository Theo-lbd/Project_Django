from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, Avg, Max
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .forms import QuestionForm
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def all_questions(request):
    all_questions_list = Question.objects.all()
    context = {"all_questions_list": all_questions_list}
    return render(request, "polls/all_questions.html", context)


def frequency(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    choices = question.get_choices()

    total_votes = sum(choice.votes for choice in choices)

    context = {
        "question": question,
        "choices": choices,
        "total_votes": total_votes,
    }
    return render(request, "polls/frequency.html", context)

def statistics(request):
    # Nombre total de sondages enregistrés
    total_polls = Question.objects.count()

    # Nombre total de choix possibles
    total_choices = Choice.objects.count()

    # Nombre total de votes
    total_votes = Choice.objects.aggregate(Sum('votes'))['votes__sum'] or 0

    # Moyenne du nombre de votes par sondage
    avg_votes_per_poll = (
        Question.objects.annotate(total_votes=Sum('choice__votes'))
        .aggregate(Avg('total_votes'))['total_votes__avg'] or 0
    )

    # Dernière question enregistrée
    latest_question = Question.objects.latest('pub_date')

    # Optionnel : Question la plus populaire (ayant reçu le plus de votes)
    most_popular_question = (
        Question.objects.annotate(total_votes=Sum('choice__votes'))
        .order_by('-total_votes')
        .first()
    )

    # Optionnel : Question la moins populaire (ayant reçu le moins de votes)
    least_popular_question = (
        Question.objects.annotate(total_votes=Sum('choice__votes'))
        .order_by('total_votes')
        .first()
    )

    context = {
        "total_polls": total_polls,
        "total_choices": total_choices,
        "total_votes": total_votes,
        "avg_votes_per_poll": avg_votes_per_poll,
        "latest_question": latest_question,
        "most_popular_question": most_popular_question,
        "least_popular_question": least_popular_question,
    }

    return render(request, "polls/statistics.html", context)


def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})