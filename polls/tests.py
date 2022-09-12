import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):
    """
    Create test cases of methods of Question model.
    """
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for quesiton 
        whose pub_date is in the future.      
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for question
        whose pub_date is older than 1 day. 
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for question
        whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for quesiton 
        whose pub_date is in the future.      
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_recently_with_old_question(self):
        """
        is_published() returns True for question
        whose pub_date is older than 1 day. 
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_recently_with_recent_question(self):
        """
        is_published() returns True for question
        whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote_with_future_question(self):
        """
        can_vote() returns False for question whose
        pub_date is in the future.
        """
        start_time = timezone.now() + datetime.timedelta(days=30)
        end_time = timezone.now() + datetime.timedelta(days=32)
        future_question = Question(pub_date=start_time, end_date=end_time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_on_publish_date(self):
        """
        can_vote() returns True if current date/time is exactly the
        question pub_date.
        """
        start_time = timezone.now()
        end_time = timezone.now() + datetime.timedelta(days=30)
        new_question = Question(pub_date=start_time, end_date=end_time)
        self.assertIs(new_question.can_vote(), True)

    def test_can_vote_on_ending_date(self):
        """
        can_vote() returns True if current date/time is exactly the
        question end_date.
        """
        start_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end_time = timezone.now()
        ending_question = Question(pub_date=start_time, end_date=end_time)
        self.assertIs(ending_question.can_vote(), True)

    def test_can_vote_after_ending_date(self):
        """
        can_vote() returns False for whose votes are after the
        question end_date.
        """
        start_time = timezone.now() - datetime.timedelta(days=2, seconds=1)
        end_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        closed_question = Question(pub_date=start_time, end_date=end_time)
        self.assertIs(closed_question.can_vote(), False)

    def test_can_vote_with_no_ending_date(self):
        """
        can_vote() returns True for question whose
        has no end_date.
        """
        start_time = timezone.now() - datetime.timedelta(days=2, seconds=1)
        new_question = Question(pub_date=start_time)
        self.assertIs(new_question.can_vote(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """
    Create test cases of Question index view.
    """
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """
    Create test cases of Question detail view.
    """
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
