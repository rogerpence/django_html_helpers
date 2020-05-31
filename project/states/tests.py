from django.test import TestCase
from bs4 import BeautifulSoup
from core import html_helpers
# Run with:
#     dj test states.tests
# Create your tests here.
class StatesTests(TestCase):

    def get_states(self):
        return [
            {
                'id': 1,
                'province': 'Alabama',
                'abbreviation': 'AL'
            },
            {
                'id': 2,
                'province': 'Indiana',
                'abbreviation': 'IN'
            },
            {
                'id': 3,
                'province': 'Colorado',
                'abbreviation': 'CO'
            },
        ]

    def test_create_tag(self):
        # expected_tag = '<select id="state" name="state" class="m-32 px-4 center">'
        select_tag_attrs = {
            'id' : 'state',
            'name': 'state',
            'class': 'm-32 px-4 center',
        }
        created_tag = html_helpers.create_tag('select', **select_tag_attrs)
        soup = BeautifulSoup(created_tag, features="html.parser")
        self.assertTrue(soup.find('select', {'name': 'state', 'class': 'm-32 px-4 center'}))

    def test_create_tag_with_no_attributes(self):
        expected_tag = '<select>'
        select_tag_attrs = {}
        created_tag = html_helpers.create_tag('select', **select_tag_attrs)
        self.assertEqual(created_tag, expected_tag)

    def test_create_options_tag_with_string_value(self):
        option_tag_attrs = {
            'class': 'text-bold'
        }

        created_tag = html_helpers.create_options_list(items = self.get_states(),
                                               text_field = 'province',
                                               value_field = 'abbreviation',
                                               selected_value = 'IN',
                                               option_tag_attrs = option_tag_attrs)

        soup = BeautifulSoup(created_tag, features="html.parser")

        tag = soup.find('option', {**option_tag_attrs, 'value': 'AL'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {**option_tag_attrs, 'value': 'CO'})
        self.assertTrue(tag and tag.text == 'Colorado')

        tag = soup.find('option', {**option_tag_attrs, 'value': 'IN', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Indiana')

    def test_create_select_tag_with_no_attributes(self):
        options_list = html_helpers.create_options_list(items = self.get_states(),
                                                text_field = 'province',
                                                value_field = 'abbreviation',
                                                selected_value = 'CO')

        soup = BeautifulSoup(options_list, features="html.parser")

        tag = soup.find('option', {'value': 'AL'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {'value': 'IN'})
        self.assertTrue(tag and tag.text == 'Indiana')

        tag = soup.find('option', {'value': 'CO', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Colorado')

    def test_create_options_list_with_numeric_value(self):
        options_list = html_helpers.create_options_list(items = self.get_states(),
                                                text_field = 'province',
                                                value_field = 'id',
                                                selected_value = 3)

        soup = BeautifulSoup(options_list, features="html.parser")

        tag = soup.find('option', {'value': '1'})
        self.assertTrue(tag and tag.text == 'Alabama')

        tag = soup.find('option', {'value': '2'})
        self.assertTrue(tag and tag.text == 'Indiana')

        tag = soup.find('option', {'value': '3', 'selected': 'selected'})
        self.assertTrue(tag and tag.text == 'Colorado')

