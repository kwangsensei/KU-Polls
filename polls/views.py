from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from .models import Question, Choice, Vote
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponseNotAllowed

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
        # return Question.objects.filter(
        #     pub_date__lte=timezone.now()
        # ).order_by('-pub_date')[:5]
        return [
            q for q in Question.objects.all().order_by('question_text') 
            if q.is_published()
        ]


class DetailView(generic.DetailView):
    """
    Create Django's generic view of question's detail page.
    Using template polls/detail.html.
    DetailView use to display a detail for particular object.
    Returns detail of question page.
    """
    model = Question
    template_name = "polls/detail.html"

    # def get_queryset(self):
    #     """Excludes any questions that aren't published yet."""
    #     return Question.objects.filter(pub_date__lte=timezone.now())

    # def redirect_when_vote_false(self, request, question_id):
    #     """
    #     Redirect the visitors to back polls index view
    #     when visitors navigatesto a poll detail view
    #     when voting is not more allowed.
    #     """
    #     question = get_object_or_404(Question, pk=question_id)
    #     if not question.can_vote():
    #         messages.error(request, "Voting is disabled.")
    #         return redirect("polls/index.html")
    #     return render(request, "polls/detail.html", {
    #         "question": question,
    #     })

    def get(self, request: HttpRequest, *args, **kwargs):
        question = get_object_or_404(Question, id=kwargs['pk'])
        if not question.is_published():
            return HttpResponseNotFound()
        # get user's previously selected choice
        if request.user.is_authenticated:
            vote = get_vote_for_user(question, request.user)
            choice = vote.choice if vote and vote.choice else None
        else:
            choice = None
        # pass the question and user's choice to the template 
        # as named variables
        context = {
            "question": question,
            "selected_choice": choice
        }
        return render(request, 'polls/detail.html', context)


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
def vote(request: HttpRequest, question_id):
    """Vote for a choice on a poll. Must be a POST request."""
    question = get_object_or_404(Question, id=question_id)
    context_data = {
        "question": question,
    }
    if not question.can_vote():
        messages.error(request, "Voting not allowed for this question")
        return render(request, 'polls/detail.html', context_data)
    if request.method != 'POST':
        # this view accepts only POST
        return HttpResponseNotAllowed(['POST'], "Only POST method is allowed")
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "Please select a choice.")
        return render(request, 'polls/detail.html', context_data)
    # Create a vote or update an existing vote
    vote = get_vote_for_user(question, request.user)
    if vote:
        vote.choice = selected_choice
        messages.info(request, "Your vote was successfully updated.")
    else:
        vote = Vote(user=request.user, choice=selected_choice)
        messages.info(request, "Your vote was successfully recorded.")
    vote.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_vote_for_user(question: Question, user) -> Vote:
    """
    Return the vote by the user for a specific poll question.

    :param question: a Question to get user's vote for
    :param user: the User whose vote to find and return
    :returns: an existing vote for the user, or None if no vote for this question.
    """
    if not user.is_authenticated:
        return None
    try:
        return Vote.objects.get(user=user, choice__question=question)
    except Vote.DoesNotExist:
        # no vote yet
        return None


def remove_vote(request, question_id):
    """
    Remove the vote by the user.

    :return: redirect to the same question page.
    """
    try:
        selected_choice = Vote.objects.get(
            user=request.user,
            choice__question=question_id,
        )
        selected_choice.delete()
        messages.info(request, "Your vote was successfully removed.")
    except Vote.DoesNotExist:
        messages.info(request, "Unsuccessful remove the vote.")
    return HttpResponseRedirect(
        reverse('polls:detail', args=(question_id,))
    )
