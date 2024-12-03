# This is an app to collect and organize information about watches
__import__('pysqlite3')
# We need those lines to prevent sqlite3 issues
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import os
import streamlit as st
from crewai import Crew, Process, Agent, Task
from crewai_tools.tools.website_search.website_search_tool import WebsiteSearchTool
from crewai_tools.tools.scrape_element_from_website.scrape_element_from_website import ScrapeElementFromWebsiteTool
from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv






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
  backstory='An experienced watch researcher with a passion for uncovering insights on watches',
  tools=[WebsiteSearchTool(),ScrapeWebsiteTool(),ScrapeElementFromWebsiteTool()]
)

writer = Agent(
  role='Writer',
  goal='Draft an interesting description',
  backstory='A skilled writer with a talent for crafting compelling narratives on watches'
)

# Define your tasks

url_task = Task(
  description=f"""Your task is to visit the provided website URLs, extract the best fitting image URL from the page, and return it. 
The image URL can be found in the 'src' attribute of an <img> tag.
Use tools to handle dynamic content (if needed) and provide headers to mimic a browser.  
If the URL is relative, convert it to an absolute URL using the base URL of the website.
Use Copy Image Link.""",
  agent=researcher,
  expected_output= 'URL to an image'
    )
research_task = Task(
  description=f"""Gather relevant information on the '{model}'.
   Use official manufacturer websites as a primary information source.
   Collect all the main specification information such as movement types, power reserve, features.
   Provide a table with all the specification you can find.
   Provide a list of webpages with relevant information to the '{model}'""",
  agent=researcher,
  expected_output='Description draft'
)
writing_task = Task(
  description='Compose a compelling summary including technical data table and pictures',
  agent=writer,
  expected_output='Final Summary'
)

# Form the crew with a sequential process
report_crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, url_task, writing_task],
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