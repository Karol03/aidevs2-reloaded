from dotenv import load_dotenv


# Load modules with the tasks #
helloapi = __import__('01_helloapi')
moderation = __import__('02_moderation')
blogger = __import__('03_blogger')
liar = __import__('04_liar')
inprompt = __import__('05_inprompt')
embedding = __import__('06_embedding')
###


# Load keys for environment
load_dotenv()


# Run tasks
embedding.embedding()
