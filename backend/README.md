# ControlAgent: Automating Control System Design with LLM Agents and Domain Expertise

Control system design is a cornerstone of modern engineering, impacting sectors such as aerospace, automotive, industrial automation, power systems, and robotics. However, despite the rise of Large Language Models (LLMs) in various fields, their application in control theory remains underexplored due to its complexity and domain specificity. To address this challenge, we introduce **ControlAgent**, a framework that leverages LLM agents in conjunction with control-oriented domain expertise to automate the entire control design process.

ControlAgent translates user-defined control tasks into optimized controller designs. It encodes **expert control knowledge** and emulates **human iterative design workflows** by tuning controller parameters to meet specific requirements. The framework integrates multiple LLM agents, including a **central agent** for task distribution and **task-specific agents** for in-depth controller design based on various system dynamics. Additionally, a **Python computation agent** handles complex calculations and controller evaluations, making ControlAgent a fully automated solution for end-to-end control system design.

<p align="center">
    <img src="assets/controlagent_general_diagram.png" width="90%">
    <br> Figure: ControlAgent Framework Overview
</p>

## 🚀 Key Features

- **Multi-Agent Collaboration**: ControlAgent breaks down complex controller design into sub-tasks handled by sevearl specialized agents.
- **Iterative Design**: Combines structured memory and feedback to iteratively refine controller parameters.
- **Performance Evaluation**: Dynamically adjusts designs to meet stability, robustness, and performance criteria.

## 🌟 ControlAgent Architecture

### Agent Design
1. **Central Agent**: Distributes tasks based on user inputs and delegates them to sub-agents.
2. **Task-Specific Agents**: Incorporate domain expertise to generate initial controller designs and refine them iteratively.
3. **Python Computation Agent**: Performs numerical computations for reliable controller synthesis and evaluations.

### Iterative Design Process

ControlAgent mimics the iterative workflows of control engineers. Instead of storing complete historical outputs, it utilizes a **structured memory buffer** that retains only key parameters and performance metrics. This memory-efficient strategy allows the agents to focus on refining designs without context overflow. **Feedback** is also encoded into new prompts for further refinement.

The LLM agent input prompts consist of:
1. **Design Instruction**: Encodes domain-specific methodologies for robust design tuning.
2. **User Requirements**: Direct inputs provided by the user.
3. **Memory and Feedback**: Summarizes previous design performance and highlights deficiencies.
4. **Response Instruction**: Specifies the expected response format for consistent output.

## 📖 ControlEval Dataset

To evaluate ControlAgent, we created **ControlEval**, a dataset with 500 control tasks across 10 categories, covering various system types (e.g., first-order systems, second-order systems, higher-order systems, systems with delays). Each task is paired with design criteria such as closed-loop stability, settling time, and phase margin. The full dataset is available in the [ControlEval](./ControlEval) directory.

## 🎯 Demo

For demonstration purposes, we provide two notebooks that explore the design process of ControlAgent for specific control tasks:

First-order stable slow mode [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1piYofgBSI2ZjXglstMnO_2aStVqq3C6e?usp=sharing)

Second-order unstable [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/135On5sa0eTjgu_PMg6_ePqlvaf90bYew)

Users only need to provide their OpenAI API key in gpt4.py and select a task_id to explore the iterative design process of ControlAgent. For completeness, we also display detailed input prompts and responses throughout the demonstration.

## 🔧 Setup and Usage

### Prerequisites
1. Install dependencies:
   
    ```bash
    pip install -r requirements.txt
    ```
2. Insert your OpenAI API key in [gpt4.py](./gpt4.py).

### Running ControlAgent
Execute the following to run all tasks in ControlEval:

```bash
python main.py --dataset_dir "./ControlEval/"
```

If you want to run specific tasks, such as for first-order systems in fast and moderate modes, execute:
```bash
python main.py --dataset_dir "./ControlEval/" --dataset_files first_order_stable_fast_data.json first_order_stable_moderate_data.json 
```


## 📂 Directory Structure

- `subagents/`: Task-specific agents for individual control task.
- `outputs/`: Conversation logs of the ControlAgent.
- `ControlEval/`: Contains the ControlEval dataset in JSON format.
- `assets/`: Diagrams and figures illustrating the framework.


## 📚 Citation

If you find our work useful in your research, please consider citing:

```
@article{guo2024controlagent,
  title={ControlAgent: Automating Control System Design via Novel Integration of LLM Agents and Domain Expertise},
  author={Guo, Xingang and Keivan, Darioush and Syed, Usman and Qin, Lianhui and Zhang, Huan and Dullerud, Geir and Seiler, Peter and Hu, Bin},
  journal={arXiv preprint arXiv:2410.19811},
  year={2024}
}
```
