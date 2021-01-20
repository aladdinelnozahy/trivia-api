import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia1_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
                                    'postgres',
                                    '1234',
                                    'localhost:5432',
                                    self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.question = {
            'question': "who is the best egyption football player",
            'answer': "Mohammed Salah",
            'difficulty': "1",
            'category': 6
        }

    def tearDown(self):

        print("test done!")
        pass

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

    def test_delete_question_by_ID(self):
        new_question = Question(
            question=self.question['question'],
            answer=self.question['answer'],
            category=self.question['category'],
            difficulty=self.question['difficulty']
        )
        new_question.insert()
        res = self.client().delete('/questions/{}'.format(new_question.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_question(self):
        res = self.client().delete('/question/100000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_not_Created_question(self):
        # miss category from data
        self.question['category'] = None
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 400)
        self.assertTrue(data['success'], False)

    def test_get_question_in_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_404_get_question_in_category(self):
        res = self.client().get('/categories/8898989/questions')
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 404)
        self.assertTrue(data['success'], False)


    def test_get_quiz_question(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'type': 'Science', 'id': '1'},
                                                   'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_notfound_quiz_question(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'type': 'none', 'id': '8888'},
                                                   'previous_questions': []})
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 404)
        self.assertTrue(data['success'], False)

if __name__ == "__main__":
    unittest.main()
