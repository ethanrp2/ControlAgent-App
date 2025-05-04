# backend/runner.py
import os
import control as ctrl
from dotenv import load_dotenv
from central_agent import CentralAgentLLM
from instruction import central_agent_prompt, response_instruct

load_dotenv()  # for your OPENAI_API_KEY etc.

def run_control_agent_from_inputs(system_input: dict) -> dict:
    """
    Compute a controller design from a single-system description.
    system_input keys:
      - num: single float or list [b0]  ➞ numerator coeffs
      - den: list of floats [a0, a1, …]  ➞ denominator coeffs
      - tau: (optional) float delay
      - phase_margin_min: float
      - settling_time_min: float
      - settling_time_max: float
      - steadystate_error_max: float
      - scenario: str (e.g. "fast", "moderate", or custom tag)
    Returns the LLM’s JSON response as a Python dict.
    """
    # 1) unpack inputs
    b = system_input["num"]
    # if user passed a single float, wrap in list
    num = b if isinstance(b, list) else [b]
    den = system_input["den"]
    scenario = system_input.get("scenario", "custom")
    tau = system_input.get("tau", None)

    # 2) build the plant
    plant = ctrl.TransferFunction(num, den)
    plant_str = f"{plant}"
    if tau is not None:
        plant_str += f" with delay {tau}s"

    # 3) build requirement summary
    pm   = system_input["phase_margin_min"]
    stmin = system_input["settling_time_min"]
    stmax = system_input["settling_time_max"]
    ess_max = system_input["steadystate_error_max"]

    req_text = (
        f"\nDesign the controller to meet:\n"
        f" • Phase margin ≥ {pm}°\n"
        f" • Settling time between {stmin}–{stmax} s\n"
        f" • Steady-state error ≤ {ess_max}\n"
    )

    # 4) thresholds for feedback
    thresholds = {
        "phase_margin":      {"min": pm,      "message": f"Phase margin ≥ {pm}° required."},
        "settling_time_min": {"min": stmin,   "message": f"Settling time ≥ {stmin}s required."},
        "settling_time_max": {"max": stmax,   "message": f"Settling time ≤ {stmax}s required."},
        "steadystate_error": {"max": ess_max, "message": f"Steady-state error ≤ {ess_max} required."},
    }

    # 5) assemble the user prompt
    user_req = f"\nPlease design a controller for G(s) = {plant_str}.{req_text}"
    full_prompt = central_agent_prompt + user_req + response_instruct

    # 6) call the LLM agent
    agent = CentralAgentLLM()
    raw = agent.assign_task(system_input, full_prompt, thresholds, scenario)

    # 7) return the JSON-parsed response
    return raw  # assume it’s already a dict; if string, json.loads(raw)








# import control as ctrl
# import json
# import argparse
# from central_agent import CentralAgentLLM
# import os
# from instruction import central_agent_prompt, response_instruct

# from dotenv import load_dotenv
# load_dotenv()

# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--engine', type=str, default='gpt-4o-2024-08-06')
#     parser.add_argument('--dataset_dir', type=str, default="./ControlEval/")
#     parser.add_argument('--dataset_files', nargs='+', help='List of dataset file names', default=None)
#     args = parser.parse_args()
#     return args

# def process_dataset(file_path):
#     with open(file_path, 'r') as f:
#         dataset = json.load(f)
    
#     for system in dataset[0:2]:  # Loop through first two systems; adjust as necessary
#         scenario = system['scenario']
#         # Provide the plant transfer function
#         num = [system['num'][0]]
#         den = system['den']
#         try:
#             tau = system['tau']
#             system_w_delay = True
#         except:
#             system_w_delay = False
#         plant = ctrl.TransferFunction(num, den)
        
#         # Define performance requirements
#         phase_margin_min = system['phase_margin_min']
#         settling_time_min = system['settling_time_min']
#         settling_time_max = system['settling_time_max']
#         steadystate_error_max = system['steadystate_error_max']

#         # Feedback
#         thresholds = {
#             'phase_margin': {'min': phase_margin_min, 'message': f'Phase margin should be at least {phase_margin_min} degrees.'},
#             'settling_time_min': {'min': settling_time_min, 'message': f'Settling time should be at least {settling_time_min} sec.'},
#             'settling_time_max': {'max': settling_time_max, 'message': f'Settling time should be at most {settling_time_max} sec.'},
#             'steadystate_error': {'max': steadystate_error_max, 'message': f'Steady state error should be at most {steadystate_error_max}.'}
#         }

#         requirements_summary = "\nDesign the controller to meet the following specifications: \n"
#         requirements_summary += f"Phase margin greater or equal {phase_margin_min} degrees, \n"
#         requirements_summary += f"Settling time greater or equal {settling_time_min} sec, \n"
#         requirements_summary += f"Settling time should also be less or equal to {settling_time_max} sec, \n"
#         requirements_summary += f"Steady state error less or equal {steadystate_error_max}. \n"
        
#         if system_w_delay:
#             user_request = "\nPlease design the controller for the following system: " +  str(plant) + f" with time delay {tau} sec" + requirements_summary
#         else:
#             user_request = "\nPlease design the controller for the following system: " +  str(plant) + requirements_summary

#         prompt = central_agent_prompt + user_request + response_instruct

#         # Instantiate the central agent
#         central_agent = CentralAgentLLM()

#         # Assign task based on LLM output
#         response = central_agent.assign_task(system, prompt, thresholds, scenario)
#         print(f"Response for dataset {file_path} and system {system['scenario']}:\n{response}\n")

# # if __name__ == "__main__":
# #     args = parse_args()
    
# #     # If dataset files are provided, use them, otherwise process all JSON files in the dataset directory
# #     if args.dataset_files:
# #         dataset_files = [os.path.join(args.dataset_dir, file) for file in args.dataset_files]
# #     else:
# #         dataset_files = [os.path.join(args.dataset_dir, file) for file in os.listdir(args.dataset_dir) if file.endswith('.json')]
    
# #     # Iterate through each dataset file
# #     for dataset_file in dataset_files:
# #         print(f"Processing dataset: {dataset_file}")
# #         process_dataset(dataset_file)

# def run_control_agent(dataset_dir="./ControlEval/", dataset_files=None):
#     if dataset_files:
#         dataset_paths = [os.path.join(dataset_dir, file) for file in dataset_files]
#     else:
#         dataset_paths = [os.path.join(dataset_dir, file) for file in os.listdir(dataset_dir) if file.endswith('.json')]

#     all_outputs = []
#     for dataset_file in dataset_paths:
#         print(f"Processing dataset: {dataset_file}")
#         result = process_dataset(dataset_file)
#         all_outputs.append(result)
#     return all_outputs