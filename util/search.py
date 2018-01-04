import json
from urllib.parse import urlencode
from urllib.request import urlopen
from collections import namedtuple

class SearchUtil:


    @staticmethod
    def search(params):
        Recipe = namedtuple('Recipe', field_names={'title', 'ingress', 'url', 'ingredients'})
        search_endpoint = 'https://botlersearchapi.azurewebsites.net/api/search?'
        qstr = urlencode(params)
        with urlopen(search_endpoint + qstr) as search_response:
            recipes = []
            # byte to json
            body = json.loads(search_response.read().decode(search_response.headers.get_content_charset()))
            for recipeObj in body['recipes']:
                recipe = Recipe(recipeObj['title'], recipeObj['ingress'], recipeObj['url'], recipeObj['ingredients'])
                recipes.append(recipe)
        return recipes
