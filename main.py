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
###


# Load keys for environment
load_dotenv()


# Run tasks
whoami.whoami()
