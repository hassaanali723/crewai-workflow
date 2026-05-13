from crewai import Task

def research_task(agent) -> Task:
    return Task(
        description=("Research the topic: {topic}. "
            "Gather key facts, trends, and insights."),
            expected_output="A bullet-point summary of key findings.",
            agent=agent,
    )


def writing_task(agent, context_tasks: list) -> Task:
    return Task(
       description=(
            "Using the research provided, write a 3-paragraph summary about {topic}."
        ),
            expected_output="A polished 3-paragraph article.",
            agent=agent,
            context=context_tasks,
    )


