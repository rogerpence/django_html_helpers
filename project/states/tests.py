from django.test import TestCase
from bs4 import BeautifulSoup
from core import repo
# Run with:
#     dj test states.tests
# Create your tests here.
class StatesTests(TestCase):

    def get_states(self):
        return [
            {
                'province': 'Alabama',
                'abbreviation': 'AL'
            },
            {
                'province': 'Indiana',
                'abbreviation': 'IN'
            },
            {
                'province': 'Colorado',
                'abbreviation': 'CO'
            },
        ]

    def test_create_tag(self):
        expected_tag = '<select id="state" name="state" class="m-32 px-4 center">'
        select_tag_attrs = {
            'id' : 'state',
            'name': 'state',
            'class': 'm-32 px-4 center',
        }
        created_tag = repo.create_tag('select', **select_tag_attrs)
        soup = BeautifulSoup(created_tag, features="html.parser")
        self.assertTrue(soup.find('select', {'name': 'state', 'class': 'm-32 px-4 center'}))

    def test_create_tag_with_empty_dict(self):
        expected_tag = '<select>'
        select_tag_attrs = {}
        created_tag = repo.create_tag('select', **select_tag_attrs)
        self.assertEqual(created_tag, expected_tag)

    def test_create_select_tag(self):
        select_tag_attrs = {
            'id' : 'state',
            'name': 'state',
            'class': 'm-32 px-4 center'
        }

        option_tag_attrs = {
            'class': 'text-bold'
        }

        current_state = 'AL'

        created_tag = repo.create_select_tag(self.get_states(),
                                            'province',
                                            'abbreviation',
                                            current_state,
                                            select_tag_attrs,
                                            option_tag_attrs)

        soup = BeautifulSoup(created_tag, features="html.parser")

        self.assertTrue(soup.find('select', select_tag_attrs))

        tag = soup.find('option', {**option_tag_attrs, 'value': 'AL', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {**option_tag_attrs, 'value': 'IN'})
        self.assertTrue(tag and tag.text == 'Indiana')

        tag = soup.find('option', {**option_tag_attrs, 'value': 'CO'})
        self.assertTrue(tag and tag.text == 'Colorado')


    def test_create_select_tag_with_no_attributes(self):
        current_state = 'AL'

        created_tag = repo.create_select_tag(self.get_states(),
                                            'province',
                                            'abbreviation',
                                            current_state)

        soup = BeautifulSoup(created_tag, features="html.parser")

        self.assertTrue(soup.find('select'))

        tag = soup.find('option', {'value': 'AL', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {'value': 'IN'})
        self.assertTrue(tag and tag.text == 'Indiana')

        tag = soup.find('option', {'value': 'CO'})
        self.assertTrue(tag and tag.text == 'Colorado')

    def test_create_select_tag_with_select_tag_attributes_only(self):
        select_tag_attrs = {
            'id': 'states'
        }

        current_state = 'AL'

        created_tag = repo.create_select_tag(self.get_states(),
                                            'province',
                                            'abbreviation',
                                            current_state,
                                            select_tag_attrs)

        soup = BeautifulSoup(created_tag, features="html.parser")

        self.assertTrue(soup.find('select', select_tag_attrs))

        tag = soup.find('option', {'value': 'AL', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {'value': 'IN'})
        self.assertTrue(tag and tag.text == 'Indiana')

        tag = soup.find('option', {'value': 'CO'})
        self.assertTrue(tag and tag.text == 'Colorado')

    def test_create_select_tag_with_option_tag_attributes_only(self):
        option_tag_attrs = {
            'class': 'abc def'
        }

        current_state = 'AL'

        # Note you have to pass an empty dictionary for the omitted
        # select tag attributes if you want to skip them but provide
        # option tag attributes.
        created_tag = repo.create_select_tag(self.get_states(),
                                            'province',
                                            'abbreviation',
                                            current_state,
                                            {},
                                            option_tag_attrs)

        soup = BeautifulSoup(created_tag, features="html.parser")

        self.assertTrue(soup.find('select'))

        tag = soup.find('option', {**option_tag_attrs, 'value': 'AL', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {**option_tag_attrs, 'value': 'IN'})
        self.assertTrue(tag and tag.text == 'Indiana')

        tag = soup.find('option', {**option_tag_attrs, 'value': 'CO'})
        self.assertTrue(tag and tag.text == 'Colorado')