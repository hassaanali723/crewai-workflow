from crewai import Crew, Process
from crew.agents import researcher_agent, writer_agent
from crew.tasks import research_task, writing_task

def build_crew() -> Crew:
   researcher = researcher_agent()
   writer = writer_agent()

   task1 = research_task(researcher)
   task2 = writing_task(writer, context_tasks=[task1])

   return Crew(
     agents=[researcher, writer],
     tasks=[task1, task2],
     process=Process.sequential,
     verbose=True,
   )