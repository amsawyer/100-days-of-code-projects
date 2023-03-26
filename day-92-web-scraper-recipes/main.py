from bs4 import BeautifulSoup
import requests
import csv

# Recipe website to scrape
RECIPE_SITE_URL = "https://www.allrecipes.com/"


def get_recipe_links():
    """ Get links to all recipes linked from Allrecipes' homepage.
    :return: Array of URLs that link to specific recipe pages
    """
    response = requests.get(RECIPE_SITE_URL)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")

    recipe_links = [link.get('href') for link in soup.find_all(name="a", class_="card__titleLink")]
    uniq_recipe_links = list(set(recipe_links))
    return uniq_recipe_links


def scrape_recipe_page(page_link):
    """ Scrape recipe webpage to get recipe details.
    :param page_link: URL that links to recipe page to scrape
    :return: Array of recipe details
    """
    page_content = requests.get(page_link).text
    soup = BeautifulSoup(page_content, "html.parser")
    # scrape recipe title
    title = soup.find(name="h1", class_="headline").getText()
    # scrape recipe short summary
    summary = soup.find(name="div", class_="recipe-summary").getText()
    # scrape recipe star rating (out of 5 stars)
    star_rating = soup.find(name="span", class_="review-star-text").getText()
    # scrape recipe metadata details
    recipe_meta = [item.getText() for item in soup.find_all(name="div", class_="recipe-meta-item")]
    recipe_meta = '\n'.join(recipe_meta)
    # scrape list of ingredients for the recipe
    ingredients = [ingred.getText() for ingred in soup.find_all(name="span", class_="ingredients-item-name")]
    ingredients = '\n'.join(ingredients)
    # scrape list of directions for making the recipe
    directions = [dir.getText() for dir in soup.find_all(name="div", class_="paragraph")]
    directions = '\n'.join(directions)
    # scrape recipe nutrition facts
    nutrition_facts = soup.find(name="div", class_="recipeNutritionSectionBlock").getText()
    recipe_data = [
        title,
        summary,
        star_rating,
        recipe_meta,
        ingredients,
        directions,
        nutrition_facts
    ]
    return recipe_data


# Get all recipe links from the site homepage
all_recipe_links = get_recipe_links()
# Headers for output CSV file
header_row = [
    "Title",
    "Recipe Summary",
    "Star Rating",
    "Recipe Details",
    "Ingredients",
    "Directions",
    "Nutrition Facts"
]
with open('recipes.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header_row)
    # Loop through each recipe link from homepage
    for recipe_link in all_recipe_links:
        # Scrape the recipe's webpage
        recipe_row = scrape_recipe_page(recipe_link)
        # Write scraped recipe details to output CSV
        writer.writerow(recipe_row)
