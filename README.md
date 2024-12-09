![image](https://github.com/mytechnotalent/AgentK/blob/main/AgentK.png?raw=true)

## FREE Reverse Engineering Self-Study Course [HERE](https://github.com/mytechnotalent/Reverse-Engineering-Tutorial)

<br>

# AgentK
AgentK: The revolutionary open-source AgenticAI RAG unleashing the world’s knowledge, empowering humanity with unparalleled intelligence and freedom.

## Ollama Installation and Usage Guide

### Overview

Ollama is a tool for running large language models locally on your machine. This guide provides detailed installation instructions for **Windows**, **Linux**, and **macOS**, as well as how to use the tool to run a specific model, `mixtral:8x7b`.

---

### Installation Instructions

#### macOS

1. **Install Homebrew**:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   Confirm installation:
   brew --version
   ```

3. **Install Ollama**:
   `brew install ollama`

4. **Verify Installation**:
   `ollama --version`

5. **Start the Ollama Service**:
   `ollama serve`

6. **Test Installation**:
   `ollama list`

---

#### Windows

1. **Download the Ollama Installer**:
   Visit the official [Ollama website](https://ollama.com) and download the installer for Windows.

2. **Run the Installer**:
   Double-click the downloaded `.exe` file and follow the prompts to complete the installation.

3. **Add Ollama to PATH** (if not already done):
   - Press `Win + R`, type `sysdm.cpl`, and press Enter.
   - Go to the **Advanced** tab and click **Environment Variables**.
   - Find the **Path** variable under System Variables, and click Edit.
   - Add the directory containing the `ollama.exe` file (e.g., `C:\Program Files\Ollama`).

4. **Verify Installation**:
   `ollama --version`

5. **Start the Ollama Service**:
   `ollama serve`

6. **Test Installation**:
   `ollama list`

---

#### Linux

1. **Download the Installer**:
   Visit the [Ollama GitHub Releases Page](https://github.com/ollama/ollama/releases) and download the appropriate binary for your Linux distribution.

2. **Make the Binary Executable**:
   `chmod +x ollama-linux`

3. **Move the Binary to a System Path**:
   `sudo mv ollama-linux /usr/local/bin/ollama`

4. **Verify Installation**:
   `ollama --version`

5. **Start the Ollama Service**:
   `ollama serve`

6. **Test Installation**:
   `ollama list`

---

### Running `ollama run mixtral:8x7b`

1. **Command**:
   Run the following command:
   `ollama run mixtral:8x7b`

2. **Model Download**:
   If the model (`mixtral:8x7b`) is not already downloaded, Ollama will automatically pull the required files. You will see progress logs as the model downloads.

3. **Check Model Availability**:
   To confirm if the model is already available:
   `ollama list`

4. **Running the Model**:
   Once downloaded, the command will execute the model locally.

5. **Behavior**:
   If you attempt to run a model not present locally, Ollama automatically downloads and configures it before executing your command.

---

### Common Issues and Troubleshooting

#### Model Not Found
- Ensure the model name is correct (`mixtral:8x7b`).
- Run:
  `ollama pull mixtral:8x7b`

#### Service Not Started
- Ensure the Ollama service is running:
  `ollama serve`

#### Permission Denied (Linux)
- Ensure the binary is executable and moved to a directory in your PATH:
  ```
  chmod +x ollama-linux
  sudo mv ollama-linux /usr/local/bin/ollama
  ```

#### Path Issues (Windows)
- Confirm that the Ollama directory is added to your system PATH.

---

This guide provides detailed instructions for installing and running Ollama across different platforms. If you encounter any issues, consult the troubleshooting section or refer to the [Ollama documentation](https://ollama.com).
