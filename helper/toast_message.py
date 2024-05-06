import random

TOAST_MESSAGES = [
    ("Here's to hoping your job search is shorter than a Vine video!", "🍷"),
    ("May your resume be as impressive as your LinkedIn profile!", "🤩"),
    ("Here's to finding a job that doesn't require a coffee IV drip!", "☕"),
    ("May your job search be as successful as your last Tinder date!", "💘"),
    ("Here's to finding a job that pays you more than your parents think you're worth!", "💰"),
    ("May your job search be as easy as finding a parking spot at the mall on Black Friday!", "🚗"),
    ("Here's to finding a job that doesn't make you want to hit snooze on Monday mornings!", "😴"),
    ("May your resume be as impressive as your Instagram feed!", "📸"),
    ("Here's to finding a job that doesn't require you to wear pants!", "🩳"),
    ("May your job search be as successful as your last Amazon Prime delivery!", "📦"),
    ("Here's to finding a job that doesn't make you want to throw your computer out the window!", "🖥️"),
    ("May your job search be as easy as ordering pizza online!", "🍕"),
    ("Here's to finding a job that doesn't require you to talk to people before noon!", "☀️"),
    ("May your resume be as impressive as your Bitmoji avatar!", "👩‍💼"),
    ("Here's to finding a job that doesn't make you want to take up day drinking!", "🍹"),
    ("May your job search be as successful as your last Instagram post!", "📱"),
    ("Here's to finding a job that doesn't require you to wear a tie!", "👔"),
    ("May your job search be as easy as finding a needle in a haystack!", "🧵"),
    ("Here's to finding a job that doesn't make you want to throw your phone across the room!", "📱"),
    ("May your resume be as impressive as your TikTok dance moves!", "💃"),
    ("Here's to finding a job that doesn't require you to work weekends!", "📅"),
    ("May your job search be as successful as your last Uber ride!", "🚗"),
    ("Here's to finding a job that doesn't make you want to take up meditation!", "🧘"),
    ("May your job search be as easy as finding a parking spot at the airport on Thanksgiving!", "🛬"),
    ("Here's to finding a job that doesn't require you to wear high heels!", "👠"),
    ("May your resume be as impressive as your Twitter following!", "🐦"),
    ("Here's to finding a job that doesn't make you want to take up knitting!", "🧶"),
    ("May your job search be as successful as your last Netflix binge!", "📺"),
    ("Here's to finding a job that doesn't require you to wear a suit!", "🕴️"),
    ("May your job search be as easy as finding a four-leaf clover!", "🍀")
]

def get_random_toast():
    """Returns a random toast message and icon."""
    return random.choice(TOAST_MESSAGES)
