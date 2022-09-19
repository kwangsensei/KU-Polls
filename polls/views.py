from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django.views import generic
from django.urls import reverse
from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    """
    Create Django's generic view of index page. 
    Using template polls/index.html.
    ListView use to display a list of objects.
    Returns a list of questions.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    Create Django's generic view of question's detail page.
    Using template polls/detail.html.
    DetailView use to display a detail for particular object.
    Returns detail of question page.
    """
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def redirect_when_vote_false(self, request, question_id):
        """
        Redirect the visitors to back polls index view when visitors navigates
        to a poll detail view when voting is not more allowed.
        """
        question = get_object_or_404(Question, pk=question_id)
        if not question.can_vote():
            messages.error(request, "Voting is disabled.")
            return redirect("polls/index.html")
        return render(request, "polls/detail.html", {
            "question": question,
        })


class ResultsView(generic.DetailView):
    """
    Create Django's generic view of vote results page.
    Using template polls/results.html.
    DetailView use to display a detail for particular object.
    Returns vote results of question page.
    """
    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    """
    Get voted choice from the visitors and redirect them to polls results view.
    If visitors did not select any choice of poll, returns detail view
    of that poll and display the error message.
    """
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after succesfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
