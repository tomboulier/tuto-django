import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
	"""
	Create a question with the given `question_text` and published the
	given number of `days` offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	"""
	pub_date = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionIndexViewTests(TestCase):
	"""Testing views"""

	def get_polls_index(self):
		"""Will be used several times below"""
		return self.client.get(reverse("polls:index"))

	def test_no_questions(self):
		"""
		If no questions exist, an appropriate message is displayed.
		"""
		response = self.get_polls_index()
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		"""
		Questions with a pub_date in the past are displayed on the
		index page.
		"""
		past_question = create_question(question_text="past question", days=-30)
		response = self.get_polls_index()
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[past_question])

	def test_future_question(self):
		"""
		Questions with a pub_date in the future aren't displayed on
		the index page.
		"""
		future_question = create_question(question_text="future question", days=+30)
		response = self.get_polls_index()
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[])

	def test_future_question_and_past_question(self):
		"""
		Even if both past and future questions exist, only past questions
		are displayed.
		"""
		past_question = create_question(question_text="past question", days=-30)
		future_question = create_question(question_text="future question", days=+30)
		response = self.get_polls_index()
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[past_question])

	def test_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		"""
		question_1 = create_question(question_text="question 1", days=0)
		question_2 = create_question(question_text="question 2", days=0)
		future_question = create_question(question_text="future question", days=+30)
		response = self.get_polls_index()
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question_2, question_1])


class QuestionDetailViewTests(TestCase):
	def get_detail_view_response(self, question):
		"""
		Will be used several times below (DRY principles).
		Return the response when getting the detail view of
		a given question.
		"""
		url = reverse("polls:detail", kwargs={'pk': question.id})
		return self.client.get(url)
		
	def test_future_question(self):
		"""
		The detail view of a question with a pub_date in the future
		returns a 404 not found.
		"""
		future_question = create_question(question_text="future question", days=0.1)
		response = self.get_detail_view_response(future_question)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		"""
		The detail view of a question with a pub_date in the past
		displays the question's text.
		"""
		text_to_display = "text to display"
		old_question = create_question(question_text=text_to_display, days=-0.1)
		response = self.get_detail_view_response(old_question)


class QuestionModelTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() returns False for questions
		whose pub_date is in the future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() returns False for questions whose pub_date
		is older than 1 day.
		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() returns True for questions whose pub_date
		is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=23)
		recently_published_question = Question(pub_date=time)
		self.assertIs(recently_published_question.was_published_recently(), True)