# Mother Agent

This project is designed to create AI agents that can dynamically generate tools and execute tasks based on a given problem statement. The agents and tools are generated using OpenAI's GPT-4 model and the CrewAI framework.

## Prerequisites

- Python 3.8 or higher
- OpenAI API Key
- Required Python packages:
  - `langchain_openai`
  - `crewai`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/mother-agent.git
    cd mother-agent
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set your OpenAI API Key in the environment:
    ```sh
    export OPENAI_API_KEY="your-openai-api-key"
    ```

## Usage

1. Run the [mother-agent-01.py](http://_vscodecontentref_/1) script:
    ```sh
    python mother-agent-01.py
    ```

2. Enter the problem statement when prompted.


## Example

Here is an example of how to use the project:

1. Run the [mother-agent-tool.py](http://_vscodecontentref_/3) script:
    ```sh
    python mother-agent-tool.py
    ```

2. Enter the problem statement:
    ```
    Please enter the problem statement: Compare the stock prices of Google and Microsoft over the last week and generate a report.
    ```


## Project Structure

- `mother-agent-01.py`: Main script to generate agents and tools.
- `Toolfactory-01.py`: Contains the `ToolFactory` and `AIAgent` classes.
problem statement.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.