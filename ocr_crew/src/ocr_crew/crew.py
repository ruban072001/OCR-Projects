from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.easy1tool import easy1_tool
from tools.padtool import paddle_tool
from crewai_tools import FileWriterTool
from dotenv import load_dotenv
load_dotenv()
# from ocr_crew.src.ocr_crew.tools.paratool import easy2_tool
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

easy1 = easy1_tool()

pad = paddle_tool()

@CrewBase
class OcrCrew():
	"""OcrCrew crew"""


	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


	@agent
	def agent1(self) -> Agent:
		return Agent(
			config=self.agents_config['agent1'],
   			tools=[easy1, pad],
			verbose=True
		)

	@agent
	def agent2(self) -> Agent:
		return Agent(
			config=self.agents_config['agent2'],
			verbose=True
		)
	
	@agent
	def agent3(self) -> Agent:
		return Agent(
			config=self.agents_config['agent3'],
			verbose=True
		)
  
	@agent
	def agent4(self) -> Agent:
		return Agent(
			config=self.agents_config['agent4'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def agent1task(self) -> Task:
		return Task(
			config=self.tasks_config['agent1task'],
		)

	@task
	def agent2task(self) -> Task:
		return Task(
			config=self.tasks_config['agent2task'],
		)

	@task
	def agent3task(self) -> Task:
		return Task(
			config=self.tasks_config['agent3task'],
		)

	@task
	def agent4task(self) -> Task:
		return Task(
			config=self.tasks_config['agent4task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the OcrCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
