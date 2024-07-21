from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
#from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool,WebsiteSearchTool, ScrapeWebsiteTool
#import streamlit as st
#from src.finagent.tools.custom_tool import MyCustomTool


#from langchain.llms import Ollama
# Uncomment the following line to use an example of a custom tool
# from ai_fin_latest.tools.custom_tool import MyCustomTool
# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
# Initialize the tool for internet searching capabilities

@CrewBase
class finagent:
    """finagent crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    def __init__(self) -> None:
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        #self.groq_llm = ChatGroq(temperature=0.3, model_name="mixtral-8x7b-32768")
        #self.groq_llm = ollama_mixtral

   # def __init__(self):
    # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
     #self.Ollama = Ollama(model="openhermes")

    @agent
    def FactCheckingSpecialist(self) -> Agent:
        return Agent(
            config=self.agents_config['FactCheckingSpecialist'],
            llm=self.OpenAIGPT35,
            tools=[SerperDevTool()], # Example of custom tool, loaded on the beginning of file
            verbose=True,
			allow_delegation=True
        )

    @agent
    def ExecutivePoliticalScientist(self) -> Agent:
        return Agent(
            config=self.agents_config['ExecutivePoliticalScientist'],
            llm=self.OpenAIGPT35,
            #tools=[SerperDevTool()],
            verbose=True,
			allow_delegation=False
        )

    @agent
    def SeniorInvestigativeJournalistandContentStrategist(self) -> Agent:
        return Agent(
            config=self.agents_config['SeniorInvestigativeJournalistandContentStrategist'],
            llm=self.OpenAIGPT35,
            #tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            verbose=True,
			allow_delegation= False
        )

   
    @task
    def researchfact_task(self) -> Task:
        return Task(
            config=self.tasks_config['researchfact_task'],
            agent=self.FactCheckingSpecialist()
        )

    @task
    def Political_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['Political_analysis'],
            agent=self.ExecutivePoliticalScientist(),
			human_input=True
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.SeniorInvestigativeJournalistandContentStrategist(),
			output_file='report.md'
        )


    @crew
    def crew(self) -> Crew:
        """Creates the AIgent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
			memory=False,
            max_rpm=500,
            verbose=2

            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )