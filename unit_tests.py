import unittest
from flask_testing import TestCase
from flask import url_for
from app.__init___ import create_app, db
from app.models import User, Gift


class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///wishlist_test.db'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test user
        user = User(
            id=1,
            email='actioncrash@mail.ru',
            username='Mykl',
            first_name='Mikhail',
            last_name='Knyazev',
            password='password',
        )

        # create test gift
        gift_1 = Gift(name='test_gift1', price=5000, url='test_url_1', user_id=1)
        gift_2 = Gift(name='test_gift2', price=6000, url='test_url_2', user_id=1)
        gift_3 = Gift(name='test_gift3', price=7000, url='test_url_3', user_id=1)

        # save users to database
        db.session.add(user)
        db.session.add(gift_1)
        db.session.add(gift_2)
        db.session.add(gift_3)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in Users table
        """
        self.assertEqual(User.query.count(), 1)

    def test_gift_model(self):
        """
        Test number of records in Gifts table
        """
        self.assertEqual(Gift.query.count(), 3)

    def test_count_gifts_for_user(self):
        """
        Test for the number of gifts the user has
        """
        self.assertEqual(Gift.query.filter_by(user_id=1).order_by(Gift.date.desc()).count(), 3)


class TestViews(TestBase):

    def test_login_views(self):
        """
        Test that login page is accessible without login
        """

        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_register_views(self):
        """
        Test that login page is register
        """
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)

    def test_index_views(self):
        """
        Test that login page is start page
        """
        response = self.client.get(url_for('gift_list.index'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()