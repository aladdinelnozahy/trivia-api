import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):

        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['questions']))

    def test_404_paginated_questions(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_question(self):
        res = self.client().delete('/question/100000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')


    def test_400_not_Created_question(self):
        self.question['category'] = None
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 400)
        self.assertTrue(data['success'], False)
        self.assertEqual(data['message'], "Error 'not allowed' ")
        self.assertEqual(data['error'], 400)

    def test_405_notAllowed_to_create_question(self):
        res = self.client().post('/questions/', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Method not allowed")
        self.assertEqual(data['error'], 405)
    
    def test_get_quiz_questions(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        res = self.client().post('/quizzes', data=json.dumps(request_data),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        if data.get('question', None):
            self.assertNotIn(data['question']['id'],
                             request_data['previous_questions'])


    def test_play_quiz_questions(self):
        """Tests playing quiz questions"""
        request_data = {
            'previous_questions': [1, 7],
            'quiz_category': {
                'type': 'Science',
                'id':3
            }
        }
        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 10)

        self.assertEqual(data['question']['category'], 4)

    def test_error_get_quiz_questions(self):
        res = self.client().post('/quizzes', data=json.dumps({}),
                                 content='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()