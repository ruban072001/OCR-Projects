from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ocragent():
	"""Ocragent crew"""
 
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def Text_Extraction_Specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['Text_Extraction_Specialist'],
			tools = [],
			verbose=True
		)

	@agent
	def Output_Format_Analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['Output_Format_Analyzer'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def Text_Extraction_Specialist_Task(self) -> Task:
		return Task(
			config=self.tasks_config['Text_Extraction_Specialist_Task'],
		)

	@task
	def Output_Format_Analyzer_Task(self) -> Task:
		return Task(
			config=self.tasks_config['Output_Format_Analyzer_Task'],

		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Ocragent crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
