import sys
import os
import re
import json
import ast
import csv
import random
import smtplib
import datetime
import subprocess
import webbrowser
import urllib.request
import urllib.parse
import importlib.util
import inspect
from email.mime.text import MIMEText
from dotenv import load_dotenv
from lark import Lark
from openai import OpenAI

# ==========================================
# 1. SETUP & SECURITY (BYOK)
# ==========================================
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if groq_key:
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key)
elif openai_key:
    client = OpenAI(api_key=openai_key)
else:
    client = None

# ==========================================
# 2. THE CORE TOOLBOX
# ==========================================
def tool_print(text=""):
    print(f"🖨️  {text}")
    return text

def tool_create_file(filename="", content="Created by Nox!"):
    if not filename: return "Error: No filename"
    safe_filename = os.path.basename(filename)
    try:
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(content) # V2 Feature: Custom content
        print(f"📁 Created file: {safe_filename}")
        return f"File {safe_filename} created."
    except Exception as e:
        print(f"❌ File Error: {e}")
        return "Error"

def tool_read_file(filename=""):
    if not filename: return "Error"
    safe_filename = os.path.basename(filename)
    try:
        with open(safe_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📄 Read file: {safe_filename}")
        return content
    except Exception as e:
        print(f"❌ File Error: {e}")
        return "Error"

def tool_parse_json(json_string="", key=""):
    if not json_string or not key: return "Error"
    try:
        data = json.loads(json_string)
        if isinstance(data, dict) and key in data:
            val = str(data[key])
            print(f"🔍 Extracted JSON key '{key}': {val}")
            return val
        print(f"⚠️ JSON key '{key}' not found.")
        return "Error"
    except Exception as e:
        print(f"❌ JSON Error: {e}")
        return "Error"

def tool_open_url(url=""):
    if not url: return "Error"
    print(f"🌐 Opening browser: {url}")
    webbrowser.open(url)
    return f"Opened {url}"

def tool_calculate(expression=""):
    if not expression: return "Error"
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        print("❌ Security Error: Invalid math characters.")
        return "Error"
    try:
        result = eval(expression)
        print(f"🔢 Calculated: {expression} = {result}")
        return str(result)
    except Exception as e:
        print(f"❌ Math Error: {e}")
        return "Error"

def tool_input(prompt=""):
    if prompt: print(f"👉 {prompt}")
    user_text = input("> ")
    return user_text

def tool_llm_think(prompt, agent_name="AI", model_name="gpt-4o-mini"):
    if not client:
        print("❌ AI Error: No API key found in .env.")
        return "Error: No API key."
    print(f"🧠 [{agent_name} using {model_name}] Thinking...")
    try:
        response = client.chat.completions.create(
            model=model_name, 
            messages=[{"role": "system", "content": f"You are {agent_name}."}, {"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        print(f"💡 AI Answer: {answer}")
        return answer
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "Error"

def tool_get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏰ Time: {now}")
    return now

def tool_random_number(max_num=""):
    try:
        limit = int(max_num) if max_num else 100
        num = random.randint(1, limit)
        print(f"🎲 Random: {num}")
        return str(num)
    except Exception as e:
        return "Error"

def tool_run_terminal(command=""):
    if not command: return "Error"
    print(f"💻 Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout if result.stdout else result.stderr
        print(f"   Output: {output.strip()[:100]}...")
        return output.strip()
    except Exception as e:
        print(f"❌ Terminal Error: {e}")
        return "Error"

def tool_scrape_webpage(url=""):
    if not url: return "Error"
    print(f"🌐 Scraping URL: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            text = re.sub('<[^<]+?>', '', html)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"   ✅ Scraped {len(text)} characters.")
            return text[:2000]
    except Exception as e:
        print(f"   ❌ Scrape Error: {e}")
        return "Error"

def tool_fetch_api(url=""):
    if not url: return "Error"
    print(f"🔌 Fetching API: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
            print(f"   ✅ Received {len(data)} chars.")
            return data
    except Exception as e:
        print(f"   ❌ API Error: {e}")
        return "Error"

def tool_download_file(url=""):
    if not url: return "Error"
    filename = os.path.basename(url) or "downloaded_file"
    print(f"📥 Downloading: {url}")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"   ✅ Saved {filename}")
        return f"Downloaded {filename}"
    except Exception as e:
        print(f"❌ Download Error: {e}")
        return "Error"

def tool_read_csv(filename=""):
    if not filename: return "Error"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        print(f"📊 Read {len(rows)} rows from {filename}.")
        return str(rows)
    except Exception as e:
        print(f"❌ CSV Error: {e}")
        return "Error"

def tool_write_csv(filename="", data=""):
    if not filename or not data: return "Error"
    try:
        parsed_data = ast.literal_eval(data) 
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(parsed_data)
        print(f"📊 Wrote to {filename}.")
        return f"Wrote to {filename}"
    except Exception as e:
        print(f"❌ CSV Write Error: {e}")
        return "Error"

def tool_send_email(to_address="", subject="", message=""):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    if not sender or not password:
        print("❌ Email Error: EMAIL_ADDRESS and EMAIL_PASSWORD missing in .env")
        return "Error"
    print(f"📧 Sending email to {to_address}...")
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_address
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("   ✅ Email Sent!")
        return "Email sent successfully"
    except Exception as e:
        print(f"❌ Email Error: {e}")
        return "Error"

def tool_send_webhook(url="", message=""):
    if not url or not message: return "Error"
    print(f"🔔 Sending webhook...")
    try:
        payload = json.dumps({"content": message, "text": message}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print("   ✅ Webhook Sent!")
            return "Webhook sent"
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        return "Error"

TOOLS = {
    "print": tool_print, "create_file": tool_create_file, "read_file": tool_read_file,
    "parse_json": tool_parse_json, "open_url": tool_open_url, "calculate": tool_calculate,
    "think": tool_llm_think, "input": tool_input, "get_time": tool_get_time,
    "random_number": tool_random_number, "run_terminal": tool_run_terminal,
    "scrape_webpage": tool_scrape_webpage, "fetch_api": tool_fetch_api,
    "download_file": tool_download_file, "read_csv": tool_read_csv,
    "write_csv": tool_write_csv, "send_email": tool_send_email, "send_webhook": tool_send_webhook
}

# ==========================================
# 3. PLUGIN SYSTEM (For Custom Tools)
# ==========================================
def load_plugins():
    """Looks for a 'plugins' folder and loads any .py files inside it."""
    plugin_dir = os.path.join(os.getcwd(), 'plugins')
    if not os.path.exists(plugin_dir):
        return
        
    print("🔌 Loading external plugins...")
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            file_path = os.path.join(plugin_dir, filename)
            
            try:
                # Dynamically load the Python file
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for functions starting with "tool_"
                for name, func in inspect.getmembers(module):
                    if inspect.isfunction(func) and name.startswith("tool_"):
                        tool_name = name[5:] # Remove "tool_" prefix
                        TOOLS[tool_name] = func
                        print(f"   ✅ Registered custom tool: {tool_name}")
            except Exception as e:
                print(f"   ❌ Failed to load plugin {filename}: {e}")

# ==========================================
# 4. THE LARK GRAMMAR (V2 Features Included)
# ==========================================
grammar = r"""
    start: statement*
    
    ?statement: agent_cmd | model_cmd | use_llm_cmd | action_cmd | save_cmd 
              | list_cmd | if_cmd | loop_cmd | foreach_cmd | while_cmd | import_cmd

    agent_cmd: "Agent is" NAME
    model_cmd: "Model is" NAME
    use_llm_cmd: "Use LLM"
    action_cmd: "Action is" NAME (STRING)*
    save_cmd: "Save result as" NAME
    
    list_cmd: "Create list" NAME "with" STRING ("," STRING)*
    
    // V2 Feature: Can now compare two variables
    if_cmd: "If" NAME OPERATOR (STRING | NAME) "then" block ("else" block)?
    OPERATOR: "is" | "==" | ">" | "<" | ">=" | "<=" | "!="
    
    loop_cmd: "Repeat" NUMBER "times" block
    foreach_cmd: "For each" NAME "in" NAME block
    while_cmd: "While" NAME OPERATOR (STRING | NAME) block
    
    block: "{" statement* "}"
    
    // V2 Feature: Import files
    import_cmd: "Import" STRING
    
    NAME: /[a-zA-Z0-9_.\/-]+/
    STRING: /"[^"]*"/
    NUMBER: /[0-9]+/
    
    COMMENT: /#[^\n]*/
    %import common.WS
    %ignore WS
    %ignore COMMENT
"""

parser = Lark(grammar, start='start')

# ==========================================
# 5. HELPER: Variable Interpolation
# ==========================================
def interpolate_variables(text, context):
    def replacer(match):
        var_name = match.group(1)
        if var_name in context:
            return str(context[var_name])
        else:
            print(f"⚠️  Warning: Variable '{{{var_name}}}' is empty or not found.")
            return match.group(0) 
    return re.sub(r'\{([a-zA-Z0-9_]+)\}', replacer, text)

# ==========================================
# 6. INTERPRETER: Execute Logic
# ==========================================
def evaluate_condition(actual_val, operator, expected_val):
    try:
        num_actual = float(actual_val)
        num_expected = float(expected_val)
        if operator in ["is", "=="]: return num_actual == num_expected
        if operator == ">": return num_actual > num_expected
        if operator == "<": return num_actual < num_expected
        if operator == ">=": return num_actual >= num_expected
        if operator == "<=": return num_actual <= num_expected
        if operator == "!=": return num_actual != num_expected
    except ValueError:
        if operator in ["is", "=="]: return actual_val == expected_val
        if operator == "!=": return actual_val != expected_val
        print(f"❌ Logic Error: Cannot use '{operator}' on text.")
        return False

def execute_block(block_node, context, current_agent, current_model, use_llm):
    last_result = None
    for stmt in block_node.children:
        result = execute_statement(stmt, context, current_agent, current_model, use_llm)
        if result is not None:
            last_result = result
    return last_result

def execute_statement(stmt, context, current_agent, current_model, use_llm):
    cmd_type = stmt.data

    if cmd_type == "agent_cmd":
        context["_agent"] = stmt.children[0].value
        print(f"🤖 Loaded Agent: {context['_agent']}")
    elif cmd_type == "model_cmd":
        context["_model"] = stmt.children[0].value
        print(f"🧠 AI Model: {context['_model']}")
    elif cmd_type == "use_llm_cmd":
        context["_use_llm"] = True
    elif cmd_type == "list_cmd":
        var_name = stmt.children[0].value
        items = [str(s)[1:-1] for s in stmt.children[1:]]
        context[var_name] = items
        print(f"📋 Created list '{var_name}' with {len(items)} items.")
        return items
    
    # V2 Feature: Import
    elif cmd_type == "import_cmd":
        file_to_import = str(stmt.children[0])[1:-1]
        if os.path.exists(file_to_import):
            print(f"📦 Importing module: {file_to_import}")
            with open(file_to_import, 'r', encoding='utf-8') as f:
                imported_code = f.read()
            try:
                imported_tree = parser.parse(imported_code)
                for imported_stmt in imported_tree.children:
                    result = execute_statement(imported_stmt, context, context.get("_agent"), context.get("_model"), context.get("_use_llm"))
                    if result is not None:
                        context["_last_result"] = result
            except Exception as e:
                print(f"❌ Syntax Error in imported file {file_to_import}: {e}")
        else:
            print(f"❌ Error: Import file '{file_to_import}' not found.")

    elif cmd_type == "action_cmd":
        tool_name = stmt.children[0].value
        raw_args = [str(arg)[1:-1] for arg in stmt.children[1:]]
        args = [interpolate_variables(arg, context) for arg in raw_args]

        if tool_name in TOOLS:
            try:
                if tool_name == "think":
                    return TOOLS[tool_name](args[0] if args else "", context.get("_agent", "AI"), context.get("_model", "gpt-4o-mini"))
                elif len(args) == 1: return TOOLS[tool_name](args[0])
                elif len(args) > 1: return TOOLS[tool_name](*args)
                else: return TOOLS[tool_name]()
            except Exception as e:
                print(f"❌ Tool Crash ({tool_name}): {e}")
        else:
            if context.get("_use_llm"):
                return tool_llm_think(f"Execute: {tool_name} {' '.join(args)}", context.get("_agent", "AI"), context.get("_model", "gpt-4o-mini"))
            else:
                print(f"⚠️ Warning: Tool '{tool_name}' does not exist. (Add 'Use LLM' to auto-route).")

    elif cmd_type == "save_cmd":
        var_name = stmt.children[0].value
        context[var_name] = context.get("_last_result", "None")
        print(f"💾 Saved to variable: {{{var_name}}}")

    elif cmd_type == "if_cmd":
        var_name = stmt.children[0].value
        operator = str(stmt.children[1]).strip('"')
        right_side_node = stmt.children[2]
        
        # V2 Feature: Check if right side is a variable or a string
        if right_side_node.type == 'STRING':
            expected_val = str(right_side_node)[1:-1]
        else:
            var_val = str(right_side_node)
            expected_val = str(context.get(var_val, ""))
            
        actual_val = str(context.get(var_name, ""))

        if evaluate_condition(actual_val, operator, expected_val):
            print(f"✅ Condition met: {var_name} {operator} '{expected_val}'")
            return execute_block(stmt.children[3], context, current_agent, current_model, use_llm)
        else:
            print(f"⏭️ Condition failed: {var_name} ('{actual_val}') is not {operator} '{expected_val}'")
            if len(stmt.children) > 4:
                return execute_block(stmt.children[4], context, current_agent, current_model, use_llm)

    elif cmd_type == "loop_cmd":
        times = int(stmt.children[0].value)
        print(f"🔁 Loop ({times}x)...")
        last_res = None
        for i in range(times):
            last_res = execute_block(stmt.children[1], context, current_agent, current_model, use_llm)
        return last_res

    elif cmd_type == "foreach_cmd":
        item_var = stmt.children[0].value
        list_name = stmt.children[1].value
        block = stmt.children[2]
        
        if list_name in context and isinstance(context[list_name], list):
            print(f"🔁 Looping through '{list_name}'...")
            last_res = None
            for item in context[list_name]:
                context[item_var] = item
                last_res = execute_block(block, context, current_agent, current_model, use_llm)
            return last_res
        else:
            print(f"❌ Error: '{list_name}' is not a valid list.")

    elif cmd_type == "while_cmd":
        var_name = stmt.children[0].value
        operator = str(stmt.children[1]).strip('"')
        right_side_node = stmt.children[2]
        
        if right_side_node.type == 'STRING':
            expected_val = str(right_side_node)[1:-1]
        else:
            var_val = str(right_side_node)
            expected_val = str(context.get(var_val, ""))
            
        block = stmt.children[3]
        
        iterations = 0
        last_res = None
        while evaluate_condition(str(context.get(var_name, "")), operator, expected_val) and iterations < 100:
            print(f"  🔄 While loop running (Iteration {iterations+1})...")
            last_res = execute_block(block, context, current_agent, current_model, use_llm)
            iterations += 1
        return last_res

# ==========================================
# 7. MAIN EXECUTION
# ==========================================
def run_bot_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {file_path}")
        return

    try:
        parse_tree = parser.parse(code)
    except Exception as e:
        print(f"❌ SYNTAX ERROR:\n{e}")
        return

    print("⚙️  Running Nox Script...\n")
    context = {}
    for stmt in parse_tree.children:
        result = execute_statement(stmt, context, context.get("_agent"), context.get("_model"), context.get("_use_llm"))
        if result is not None:
            context["_last_result"] = result

    print("\n✅ Execution Finished.")

# ==========================================
# 8. CLI ENTRY POINT
# ==========================================
def main():
    load_plugins() # Load dev plugins before running anything

    if len(sys.argv) < 2:
        print("Usage: nox <your_file.nox>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    run_bot_file(file_path)

if __name__ == "__main__":
    main()