from dotenv import load_dotenv


# Load modules with the tasks #
helloapi = __import__('01_helloapi')
moderation = __import__('02_moderation')
blogger = __import__('03_blogger')
liar = __import__('04_liar')
inprompt = __import__('05_inprompt')
embedding = __import__('06_embedding')
whisper = __import__('07_whisper')
functions = __import__('08_functions')
rodo = __import__('09_rodo')
scraper = __import__('10_scraper')
whoami = __import__('11_whoami')
search = __import__('12_search')
people = __import__('13_people')
knowledge = __import__('14_knowledge')
tools = __import__('15_tools')
gnome = __import__('16_gnome')
ownapi = __import__('17_ownapi')
###


# Load keys for environment
load_dotenv()


# Run tasks
ownapi.ownapi()
