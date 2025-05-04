import json
from gpt4 import GPT4
from subagents.first_ord_stable import first_ord_stable_Design
from subagents.first_ord_unstable import first_ord_unstable_Design
from subagents.second_ord_stable import second_ord_stable_Design
from subagents.second_ord_unstable import second_ord_unstable_Design
from subagents.first_ord_w_delay import first_ord_w_delay_Design
from subagents.higher_ord import higher_ord_Design

class CentralAgentLLM:

    def __init__(self, engine='gpt-4o-2024-08-06', temperature=0.0, max_tokens=1024):
        # Define the available sub-agents
        self.sub_agents = {
            1: first_ord_stable_Design(),
            2: first_ord_unstable_Design(),
            3: second_ord_stable_Design(),
            4: second_ord_unstable_Design(),
            5: first_ord_w_delay_Design(),
            6: higher_ord_Design()
        }
        self.gpt4 = GPT4(engine=engine, temperature=temperature, max_tokens=max_tokens)


    def assign_task(self, system, input_prompt, thresholds, scenario):
        # Parse the LLM response, which follows a strict JSON format.
        response = self.gpt4.complete(input_prompt)

        # print(f"central agent response: {response}")

        parsed_response = json.loads(response)
        agent_number = int(parsed_response.get("Agent Number"))

        if agent_number in self.sub_agents:
            sub_agent = self.sub_agents[agent_number]
            print(f"Activating sub-agent: {agent_number}")
            print( parsed_response['Task Requirement'])
            response = sub_agent.handle_task(system, thresholds, parsed_response['Task Requirement'], scenario)
        else:
            print("No suitable sub-agent found for this task.")

        

        return response

