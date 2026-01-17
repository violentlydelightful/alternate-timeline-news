#!/usr/bin/env python3
"""
Alternate Timeline News - Headlines from parallel universes
What's happening in the timelines where things went differently
"""

import random
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Timeline types
TIMELINE_NAMES = [
    "Timeline Alpha-7",
    "The Upside-Down Economy",
    "Universe B-612",
    "The Reasonable Timeline",
    "Dimension X-23",
    "The Spicy Timeline",
    "Universe Prime-ish",
    "The One Where Everything's Fine",
    "Timeline Omega",
    "The Weird One",
]

# Headline templates with [BLANKS] to fill
HEADLINE_TEMPLATES = [
    # Tech
    "[COMPANY] announces [PRODUCT] will now run on [POWER_SOURCE]",
    "[COMPANY] acquires [COUNTRY] in surprise $[BIG_NUMBER] trillion deal",
    "Scientists discover [TECH] has been [EMOTION] the whole time",
    "[COMPANY] CEO admits [PRODUCT] was just [MUNDANE_THING] all along",
    "[SOCIAL_MEDIA] introduces [WEIRD_FEATURE] to 'enhance user experience'",
    "Breaking: [TECH] achieves [IMPOSSIBLE_THING], experts concerned",
    "[COMPANY] pivots to [RANDOM_INDUSTRY], stock price [STOCK_ACTION]",

    # Politics
    "[COUNTRY] and [COUNTRY] resolve all disputes over game of [GAME]",
    "World leaders agree [MUNDANE_THING] is the real priority",
    "[POLITICIAN_TYPE] proposes mandatory [RANDOM_THING] for all citizens",
    "UN votes to classify [FOOD] as a human right",
    "International summit ends with everyone agreeing that [ANIMAL] should be in charge",

    # Science
    "Scientists confirm [THING] is actually [OTHER_THING] wearing a disguise",
    "New study reveals [FOOD] has been [EMOTION] about us for years",
    "Astronomers discover planet made entirely of [MATERIAL]",
    "Physicists prove [ABSTRACT_CONCEPT] doesn't technically exist",
    "Research shows [PERCENTAGE]% of [THING] is just [OTHER_THING]",

    # Culture
    "[CELEBRITY] reveals they've been [ANIMAL] in disguise since [YEAR]",
    "Historians discover [HISTORICAL_FIGURE] invented [MODERN_THING]",
    "[SPORT] officially adds [WEIRD_RULE] to gameplay",
    "Museum announces [ART] was actually [MUNDANE_THING]",
    "[MOVIE_GENRE] movies now required to include [RANDOM_REQUIREMENT]",

    # Economy
    "Economists stunned as [CURRENCY] backed by [RANDOM_THING]",
    "[INDUSTRY] collapses after discovery that [ABSURD_REVELATION]",
    "Stock market responds positively to news of [WEIRD_NEWS]",
    "[COMPANY] valued at $[BIG_NUMBER] trillion despite selling only [MUNDANE_THING]",

    # Absurdist
    "[THING] gains sentience, immediately [HUMAN_ACTION]",
    "Breaking: [LOCATION] confirmed to be a myth, residents confused",
    "Time travelers warn against [MUNDANE_ACTION]",
    "Simulation theory proven true, developers apologize for [BUG]",
    "[ANIMAL] elected to [POSITION] in landslide victory",
]

# Fill-in options
COMPANIES = ["Apple", "Google", "Amazon", "Microsoft", "Tesla", "Meta", "Netflix", "SpaceX", "IKEA", "Nintendo", "Costco"]
COUNTRIES = ["Denmark", "Switzerland", "New Zealand", "Canada", "Japan", "Iceland", "Portugal", "Finland", "The Moon Colony"]
PRODUCTS = ["iPhone", "self-driving cars", "smart toasters", "AI assistants", "the metaverse", "blockchain", "streaming service"]
POWER_SOURCES = ["potatoes", "human optimism", "spite", "pure chaos", "recycled dreams", "ambient frustration"]
EMOTIONS = ["disappointed", "jealous", "confused", "in love with humanity", "planning something", "mildly annoyed"]
MUNDANE_THINGS = ["three raccoons in a trenchcoat", "a very elaborate joke", "a tax write-off", "a cry for help", "organized chaos"]
TECH = ["artificial intelligence", "the internet", "cryptocurrency", "social media", "cloud computing"]
ANIMALS = ["capybara", "crow", "octopus", "golden retriever", "pigeon", "raccoon", "cat", "duck"]
FOODS = ["pizza", "avocado toast", "cheese", "bread", "coffee", "oat milk", "tacos"]
MATERIALS = ["cheese", "nostalgia", "abandoned dreams", "pure wifi", "condensed anxiety", "crystallized hope"]
THINGS = ["happiness", "success", "the economy", "friendship", "Monday mornings", "traffic", "weather"]
OTHER_THINGS = ["collective hallucination", "marketing", "several smaller problems", "quantum nonsense", "vibes"]
ABSTRACT_CONCEPTS = ["time", "gravity on Tuesdays", "the number 7", "the color beige", "Wednesdays"]
CELEBRITIES = ["A major pop star", "That one actor everyone likes", "A famous billionaire", "A beloved talk show host"]
HISTORICAL_FIGURES = ["Benjamin Franklin", "Cleopatra", "Leonardo da Vinci", "Shakespeare", "Genghis Khan"]
MODERN_THINGS = ["cryptocurrency", "memes", "podcasts", "influencer culture", "anxiety", "the concept of 'vibes'"]
SPORTS = ["Soccer", "Basketball", "Tennis", "Golf", "Chess", "Competitive sleeping"]
WEIRD_RULES = ["mandatory dance breaks", "reverse gravity periods", "emotional support animals on field", "time-outs for snacks"]
MOVIE_GENRES = ["Action", "Horror", "Rom-com", "Documentary", "Superhero"]
RANDOM_REQUIREMENTS = ["a wholesome subplot", "at least one capybara", "a 10-minute ambient soundscape", "mandatory happy ending"]
INDUSTRIES = ["crypto", "NFTs", "metaverse real estate", "artisanal water", "professional napping"]
CURRENCIES = ["the dollar", "Bitcoin", "the Euro", "social credit", "vibes"]
LOCATIONS = ["Australia", "Finland", "Wyoming", "Atlantis", "IKEA", "New Jersey"]
POSITIONS = ["mayor", "CEO", "Prime Minister", "head of HR", "Supreme Court Justice", "vibes coordinator"]
WEIRD_FEATURES = ["mandatory nap reminders", "emotional damage scoring", "existential crisis mode", "aggressive positivity filters"]
SOCIAL_MEDIA = ["Twitter", "Instagram", "TikTok", "LinkedIn", "BeReal", "Threads"]
RANDOM_INDUSTRY = ["artisanal pencils", "professional cuddling", "anxiety management", "competitive silence"]
STOCK_ACTIONS = ["inexplicably soars", "achieves consciousness", "becomes a meme", "transcends value"]
GAMES = ["Rock Paper Scissors", "Mario Kart", "Uno", "chess (but speed round)", "competitive staring"]
POLITICIAN_TYPE = ["Local mayor", "Senator", "The President's dog", "A very confident intern"]
RANDOM_THING = ["hat-wearing", "morning dance", "weekly wilderness survival", "synchronized napping"]
HUMAN_ACTIONS = ["files for divorce", "starts a podcast", "demands better representation", "applies to grad school"]
BUGS = ["the birds thing", "capitalism", "that one sound you can't identify", "Mondays", "mosquitoes"]
MUNDANE_ACTIONS = ["eating yellow foods on Thursdays", "over-organizing your desk", "replying-all", "parallel parking"]
WEIRD_NEWS = ["cats learning to type", "the moon getting slightly bigger", "nothing happening for once", "everyone being normal"]
ABSURD_REVELATIONS = ["it was just a really good dream", "birds aren't real", "nobody actually likes it", "it runs on vibes only"]
YEAR = ["1847", "1923", "1986", "2003", "the Renaissance", "next Tuesday"]
ART = ["The Mona Lisa", "Starry Night", "The Scream", "That one banana taped to a wall"]
BIG_NUMBERS = ["47", "892", "2.3", "infinity", "420"]
PERCENTAGES = ["73", "100", "47.3", "99.9", "about 60-ish"]


def fill_template(template):
    """Fill in a headline template with random options."""
    result = template

    replacements = {
        "[COMPANY]": COMPANIES,
        "[COUNTRY]": COUNTRIES,
        "[PRODUCT]": PRODUCTS,
        "[POWER_SOURCE]": POWER_SOURCES,
        "[EMOTION]": EMOTIONS,
        "[MUNDANE_THING]": MUNDANE_THINGS,
        "[TECH]": TECH,
        "[ANIMAL]": ANIMALS,
        "[FOOD]": FOODS,
        "[MATERIAL]": MATERIALS,
        "[THING]": THINGS,
        "[OTHER_THING]": OTHER_THINGS,
        "[ABSTRACT_CONCEPT]": ABSTRACT_CONCEPTS,
        "[CELEBRITY]": CELEBRITIES,
        "[HISTORICAL_FIGURE]": HISTORICAL_FIGURES,
        "[MODERN_THING]": MODERN_THINGS,
        "[SPORT]": SPORTS,
        "[WEIRD_RULE]": WEIRD_RULES,
        "[MOVIE_GENRE]": MOVIE_GENRES,
        "[RANDOM_REQUIREMENT]": RANDOM_REQUIREMENTS,
        "[INDUSTRY]": INDUSTRIES,
        "[CURRENCY]": CURRENCIES,
        "[LOCATION]": LOCATIONS,
        "[POSITION]": POSITIONS,
        "[WEIRD_FEATURE]": WEIRD_FEATURES,
        "[SOCIAL_MEDIA]": SOCIAL_MEDIA,
        "[RANDOM_INDUSTRY]": RANDOM_INDUSTRY,
        "[STOCK_ACTION]": STOCK_ACTIONS,
        "[GAME]": GAMES,
        "[POLITICIAN_TYPE]": POLITICIAN_TYPE,
        "[RANDOM_THING]": RANDOM_THING,
        "[HUMAN_ACTION]": HUMAN_ACTIONS,
        "[BUG]": BUGS,
        "[MUNDANE_ACTION]": MUNDANE_ACTIONS,
        "[WEIRD_NEWS]": WEIRD_NEWS,
        "[ABSURD_REVELATION]": ABSURD_REVELATIONS,
        "[YEAR]": YEAR,
        "[ART]": ART,
        "[BIG_NUMBER]": BIG_NUMBERS,
        "[PERCENTAGE]": PERCENTAGES,
        "[IMPOSSIBLE_THING]": ["self-awareness", "world peace", "affordable housing", "actually working", "agreeing on pizza toppings"],
    }

    for placeholder, options in replacements.items():
        while placeholder in result:
            result = result.replace(placeholder, random.choice(options), 1)

    return result


def generate_headline():
    """Generate a single headline."""
    template = random.choice(HEADLINE_TEMPLATES)
    headline = fill_template(template)

    # Generate metadata
    hours_ago = random.randint(1, 48)
    timeline = random.choice(TIMELINE_NAMES)

    categories = ["BREAKING", "DEVELOPING", "EXCLUSIVE", "ALERT", "JUST IN", "UPDATE"]

    return {
        "headline": headline,
        "timeline": timeline,
        "category": random.choice(categories),
        "time_ago": f"{hours_ago}h ago",
        "reactions": {
            "confused": random.randint(1000, 50000),
            "concerned": random.randint(500, 25000),
            "delighted": random.randint(200, 15000),
        },
    }


def generate_feed(count=10):
    """Generate multiple headlines."""
    return [generate_headline() for _ in range(count)]


@app.route("/")
def index():
    headlines = generate_feed(8)
    return render_template("index.html", headlines=headlines)


@app.route("/api/headlines")
def api_headlines():
    count = min(int(request.args.get("count", 10)), 50)
    return jsonify(generate_feed(count))


@app.route("/api/headline")
def api_single():
    return jsonify(generate_headline())


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Alternate Timeline News")
    print("=" * 50)
    print("\n  Broadcasting from parallel universes at: http://localhost:5012")
    print("  Press Ctrl+C to collapse the waveform\n")
    app.run(debug=True, port=5012)
