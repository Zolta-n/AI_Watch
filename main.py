# This is an app to collect and organize information about watches
import os
import streamlit as st
from crewai import Crew, Process, Agent, Task
from crewai_tools.tools.website_search.website_search_tool import WebsiteSearchTool
from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv


# Check if the environment variable exists
if "OPENAI_API_KEY" in os.environ:
    # Delete the environment variable
    del os.environ["OPENAI_API_KEY"]


load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI model for use with agents
openai = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)


model=st.text_input("Model", key="model")
st.button("Find", type="primary")


# Define your agents


researcher = Agent(
  role='Researcher',
  goal='Conduct foundational research on watches',
  backstory='An experienced watch researcher with a passion for uncovering insights',
  tools=[WebsiteSearchTool()]
)

writer = Agent(
  role='Writer',
  goal='Draft an interesting description',
  backstory='A skilled writer with a talent for crafting compelling narratives on watches'
)

# Define your tasks

url_task = Task(
  description=f"""find the best high quality picture for the '{model}'.
   Use the latest official manufacturer websites provide a valid link to a picture.
   Validate links availability.""",
  agent=researcher,
  expected_output= 'URL'
    )
research_task = Task(
  description=f"""Gather relevant information on the '{model}'.
   Use official manufacturer websites as a primary information source.
   Collect all the main specification information such as movement types, power reserve, features""",
  agent=researcher,
  expected_output='Description draft'
)
writing_task = Task(
  description='Compose a compelling summary with some technical data in 10 bullet points',
  agent=writer,
  expected_output='Final Summary'
)

# Form the crew with a sequential process
report_crew = Crew(
  agents=[researcher, writer],
  tasks=[url_task, research_task, writing_task],
  process=Process.sequential
)

if st.button:
    # Execute the crew
    result = report_crew.kickoff()

    url = url_task.output.raw
    #task_output = url_task.output
    #url = task_output.json_dict.get("result")

    st.write(url)


    #image_url = url
    #st.image(image_url,width=200,caption="Image from URL")

    st.markdown(result)