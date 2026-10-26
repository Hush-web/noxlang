🌘 Nox: The Language of Automation

**Nox** is a Turing-complete, Domain Specific Language (DSL) built in Python and Lark. It is designed to make building AI agents and automating complex workflows as simple as writing plain English. No brackets, no semicolons—just logic.

Whether you are a developer looking to speed up your workflow, a security analyst writing deterministic playbooks, or a founder building AI agents, Nox provides a fast, readable, and secure environment.


 ✨ Features

- **Plain English Syntax:** Write code that reads exactly like human thought.
- **Deterministic Logic:** Perfect for cybersecurity and auditing—no AI hallucinations.
- **18 Built-in Tools:** Web scraping, file I/O, JSON parsing, math, system commands, and more (using Python's standard library).
- **Optional AI Integration (BYOK):** Bring Your Own Key (Groq, OpenAI) to add LLM capabilities only when you need them.
- **Secure by Design:** Built-in path traversal protection and safe math evaluation to prevent malicious code injection.
- **Turing-Complete:** Supports nested logic, variables, lists, and advanced loops.

---

## 🚀 Installation

Nox requires Python 3.8 or higher. Install it globally via PyPI:

```bash
pip install noxlang
```

Verify the installation:

```bash
nox --help
```

---

## 🏁 Quick Start

Create a file named `hello.nox`:

```text
Agent is Greeter

Action is print "Hello, World!"
Action is input "What is your name?"
Save result as UserName

Action is print "Welcome to Nox, {UserName}!"
```

Run the script from your terminal:

```bash
nox hello.nox
```

---

## 🧠 Language Syntax

Nox is built on a few simple, intuitive commands.

### 1. Variables & Memory
Save the result of any action and inject it anywhere using `{VariableName}`.
```text
Action is calculate "50 + 50"
Save result as Total
Action is print "The final total is: {Total}"
```

### 2. Lists & Loops
Create lists and loop through them easily.
```text
Create list Cities with "Lagos", "Abuja", "Kano"

For each City in Cities {
    Action is print "Processing {City}..."
}
```

### 3. Conditional Logic (If/Else)
Make decisions based on string matching or math comparisons (`is`, `>`, `<`, `>=`, `<=`, `!=`).
```text
Action is input "Enter your age:"
Save result as Age

If Age >= "18" then {
    Action is print "Access granted."
} else {
    Action is print "Access denied."
}
```

### 4. Loops (Repeat & While)
```text
# Fixed Loop
Repeat 3 times {
    Action is print "Retrying connection..."
}

# While Loop (Includes a 100-iteration safety kill-switch)
While Status is "Running" {
    Action is print "System active..."
}
```

---

## 🧰 The Toolbox (Built-in Tools)

Nox comes pre-packaged with 18 powerful tools that require **zero extra dependencies** (uses Python standard library).

### Core Tools
| Tool | Description | Example |
| :--- | :--- | :--- |
| `print` | Display text on screen. | `Action is print "Hello"` |
| `input` | Pause script and ask user for input. | `Action is input "Name?"` |
| `calculate` | Safely evaluate math expressions. | `Action is calculate "10 * 5"` |
| `create_file` | Create a text file. | `Action is create_file "notes.txt"` |
| `read_file` | Read a text/JSON file. | `Action is read_file "data.json"` |
| `parse_json` | Extract a specific key from JSON. | `Action is parse_json "{RawData}" "status"` |
| `open_url` | Open a URL in the default browser. | `Action is open_url "https://google.com"` |

### System & Automation
| Tool | Description | Example |
| :--- | :--- | :--- |
| `get_time` | Get the current date and time. | `Action is get_time` |
| `random_number` | Generate a random number. | `Action is random_number "100"` |
| `run_terminal` | Execute shell commands (e.g., `dir`, `mkdir`). | `Action is run_terminal "dir"` |
| `scrape_webpage` | Extract text from a website. | `Action is scrape_webpage "https://news.com"` |
| `fetch_api` | Make an HTTP GET request. | `Action is fetch_api "https://api.com/data"` |
| `download_file` | Download a file from a URL. | `Action is download_file "https://site.com/file.pdf"` |
| `read_csv` | Read data from a CSV file. | `Action is read_csv "data.csv"` |
| `write_csv` | Write data to a CSV file. | `Action is write_csv "out.csv" "{Data}"` |

### Communications & AI
| Tool | Description | Example |
| :--- | :--- | :--- |
| `send_email` | Send an email via SMTP. | `Action is send_email "boss@test.com" "Subject" "Message"` |
| `send_webhook` | Send alerts to Discord/Slack. | `Action is send_webhook "https://discord..." "Alert!"` |
| `think` | Send a prompt to the LLM (Requires BYOK). | `Action is think "Write a poem"` |

---

## 🤖 AI Integration (BYOK)

Nox is 100% functional without AI. However, if you want to use the `think` tool, you must provide your own API key. 

Create a `.env` file in the same folder as your `.nox` script:

```env
# Choose one (Nox prioritizes Groq if both are present)
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
```

Then, you can build autonomous agents:
```text
Agent is Researcher
Use LLM
Model is llama-3.1-8b-instant

Action is scrape_webpage "https://en.wikipedia.org/wiki/Lagos"
Save result as WebText

Action is think "Summarize this text in 2 sentences: {WebText}"
Save result as Summary

Action is print "Summary: {Summary}"
```

---

## 🛡️ Security & Safety

Because Nox is designed for automation and potentially running on servers, security is baked in:
1. **Path Traversal Protection:** The `create_file` and `read_file` tools use `os.path.basename` to prevent users from overwriting system files (e.g., blocking `../../Windows/System32`).
2. **Safe Math:** The `calculate` tool uses a strict character whitelist, blocking malicious Python `eval()` injections.
3. **Loop Limits:** `While` loops have a hard limit of 100 iterations to prevent infinite loops from crashing your machine.

---

## 💼 Use Cases

- **Data Pipelines:** Scrape a web page -> Extract data via AI -> Save to CSV.
- **Cybersecurity:** Read server logs -> `grep` for failed passwords -> Run a firewall command -> Send a Slack alert.
- **Trading Bots:** Fetch crypto prices -> Parse JSON -> Trigger webhooks based on custom thresholds.
- **System Auditing:** Loop through local directories -> Run `dir` -> Save a timestamped report.

---

## 🤝 Contributing

Nox is open-source and built for the community. If you have ideas for new tools or language features, feel free to fork the repository, submit a pull request, or open an issue.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
```