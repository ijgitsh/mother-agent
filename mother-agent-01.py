import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew

# Ensure you have an OpenAI API Key in the environment or pass it directly
os.environ["OPENAI_API_KEY"] = ""   # Replace with your actual API key

# Initialize LLM with the correct API key
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

class AIAgent:
    def __init__(self):
        self.llm = llm

    def get_agents_and_tools(self, problem):
        decision = self.decide_agents(problem)
        agents = decision["agents"]
        roles = decision["roles"]
        relationships = decision["relationships"]
        
        tools = self.extract_tools(roles)
        
        return {"agents": agents, "tools": tools}

    def decide_agents(self, problem):
        """Uses LLM to determine necessary agents and tasks."""
        prompt = f"""
        Given the problem: "{problem}", determine:
        1. What agents are required? (e.g., ResearchAgent, ReportAgent)
        2. What does each agent do?
        3. How do they interact?
        
        Respond in a structured format:
        - Agents: [List of agent names]
        - Roles: {{AgentName: "Role description"}}
        - Relationships: {{AgentName: ["Agents it depends on"]}}
        """

        response = self.llm.invoke(prompt)
        return self.parse_response(response.content)

    def parse_response(self, response):
        """Parses the structured response into usable data."""
        lines = response.strip().split("\n")
        agents = []
        roles = {}
        relationships = {}

        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith("- Agents:"):
                current_section = "agents"
            elif line.startswith("- Roles:"):
                current_section = "roles"
            elif line.startswith("- Relationships:"):
                current_section = "relationships"
            elif current_section == "agents" and line:
                agents.append(line.replace("-", "").strip())
            elif current_section == "roles" and ":" in line:
                agent, role = line.split(":", 1)
                roles[agent.strip()] = role.strip()
            elif current_section == "relationships" and ":" in line:
                agent, dependencies = line.split(":", 1)
                relationships[agent.strip()] = [
                    dep.strip() for dep in dependencies.split(",") if dep.strip()
                ]

        return {"agents": agents, "roles": roles, "relationships": relationships}

    def extract_tools(self, roles):
        tools = []
        for role in roles.values():
            # Assuming tools are mentioned in the role description
            if "tool" in role.lower():
                tools.append(role)
        return tools

    def create_agents(self, agents_info):
        """Dynamically creates agents based on roles."""
        agents = {}
        for agent_name, role in agents_info.items():
            agents[agent_name] = Agent(
                role=role,
                goal=f"Perform {role.lower()} for the given problem.",
                backstory=f"You are an expert {role.lower()}.",
                llm=self.llm,
                user_input_handler=self.get_user_input  # Add user input handler
            )
        return agents

    def create_tasks(self, problem, agents, relationships):
        """Dynamically creates tasks and assigns dependencies."""
        tasks = {}
        for agent_name in agents:
            dependencies = relationships.get(agent_name, [])
            input_data = (
                [tasks[dep] for dep in dependencies if dep in tasks]
                if dependencies
                else None
            )
            tasks[agent_name] = Task(
                description=f"{agent_name} solves part of the problem: {problem}",
                agent=agents[agent_name],
                input=input_data,
                expected_output=f"Expected output for {agent_name} solving the problem: {problem}"  # Add expected_output field
            )
        return tasks

    def get_user_input(self, prompt):
        """Handles user input for agents."""
        return input(prompt)

    def execute(self, problem):
        """Executes the dynamically created agents and tasks."""
        decision = self.decide_agents(problem)
        agents = self.create_agents(decision["roles"])
        tasks = self.create_tasks(problem, agents, decision["relationships"])

        crew = Crew(
            agents=list(agents.values()),
            tasks=list(tasks.values()),
            verbose=True,
        )

        return crew.kickoff()

# Example Usage
if __name__ == "__main__":
    ai_agent = AIAgent()
    problem_statement = input("Please enter the problem statement: ")
    result = ai_agent.execute(problem_statement)
    
    print("Final Output:", result)