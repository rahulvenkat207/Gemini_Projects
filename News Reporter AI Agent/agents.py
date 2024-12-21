from crewai import Agent
from tools import tool

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",verbose=True,temperature = 0.5,
                             google_api_key = os.getenv("GOGGLE_API_KEY"))

## Creating a senior researcher agent

news_researcher = Agent(
    role = "Senior Researcher",
    goal= "uncover ground breaking Technologies in {topic}",
    verbose = True,
    memory = True,
    backstory = (
        "Driven by curiosity, you are at the forefront of"
        "innovation, eager to explore and share knowledge that could change the world."
    ),
    tools = [tool],
    llm= llm,
    allow_delegation = True
)

## Creating a write agent with custom tools responsible in writing new blog
news_writer = Agent(
    role = "Writer" ,
    goal= "Narrate compelling tech sotreis about {topic}",
    verbose = True,
    memory = True,
    backstory = (
        "with a flair for simplifying complex topics, you craft"
        "engagiing narratives that captivate and educate, bringing new discoveries to light in an accessible manner."
    ),
    tools = [tool],
    llm= llm,
    allow_delegation = False
)

