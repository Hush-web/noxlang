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
from email.mime.text import MIMEText
from dotenv import load_dotenv
from lark import Lark
from openai import OpenAI

# ==========================================
# 1. SETUP & SECURITY (BYOK - Groq + OpenAI)
# ==========================================
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# Check for Groq first, then OpenAI
if groq_key:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_key
    )
    print("⚡ Engine configured to use Groq (Fast & Free).")
elif openai_key:
    client = OpenAI(api_key=openai_key)
    print("🧠 Engine configured to use OpenAI.")
else:
    client = None
    print("⚠️ No API key found. LLM features will be disabled.")
# ==========================================
# 2. THE TOOLBOX (Core & Autonomous Tools)
# ==========================================
def tool_print(text=""):
    print(f"🖨️  {text}")
    return text

def tool_create_file(filename=""):
    if not filename: return "Error"
    safe_filename = os.path.basename(filename)
    with open(safe_filename, 'w', encoding='utf-8') as f:
        f.write("Created by BotLang!")
    print(f"📁 Created file: {safe_filename}")
    return f"File {safe_filename} created."

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
        print("❌ Security Error: Invalid math.")
        return "Error"
    try:
        result = eval(expression)
        print(f"🔢 Calculated: {expression} = {result}")
        return str(result)
    except Exception:
        return "Error"

def tool_input(prompt=""):
    if prompt: print(f"👉 {prompt}")
    user_text = input("> ")
    print(f"⌨️  User typed: {user_text}")
    return user_text

def tool_llm_think(prompt, agent_name="AI", model_name="gpt-4o-mini"):
    if not client:
        print("❌ ERROR: No OPENAI_API_KEY found in .env")
        return "Error"
    print(f"🧠 [{agent_name}] Thinking...")
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

# --- THE 10 AUTONOMOUS TOOLS ---

def tool_get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏰ Current time: {now}")
    return now

def tool_random_number(max_num=""):
    try:
        limit = int(max_num) if max_num else 100
        num = random.randint(1, limit)
        print(f"🎲 Random number: {num}")
        return str(num)
    except:
        return "Error"

def tool_run_terminal(command=""):
    if not command: return "Error"
    print(f"💻 Running command: {command}")
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
            print(f"   Scraped {len(text)} characters.")
            return text[:2000]
    except Exception as e:
        print(f"❌ Scrape Error: {e}")
        return "Error"

def tool_fetch_api(url=""):
    if not url: return "Error"
    print(f"🔌 Fetching API: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
            print(f"   Received {len(data)} chars.")
            return data
    except Exception as e:
        print(f"❌ API Error: {e}")
        return "Error"

def tool_download_file(url=""):
    if not url: return "Error"
    filename = os.path.basename(url) or "downloaded_file"
    print(f"📥 Downloading: {url} to {filename}")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"   Successfully saved {filename}")
        return f"Downloaded {filename}"
    except Exception as e:
        print(f"❌ Download Error: {e}")
        return "Error"

def tool_read_csv(filename=""):
    if not filename: return "Error"
    print(f"📊 Reading CSV: {filename}")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            print(f"   Found {len(rows)} rows.")
            return str(rows)
    except Exception as e:
        print(f"❌ CSV Error: {e}")
        return "Error"

def tool_write_csv(filename="", data=""):
    if not filename or not data: return "Error"
    print(f"📊 Writing to CSV: {filename}")
    try:
        # Using ast.literal_eval for safety instead of eval
        parsed_data = ast.literal_eval(data) 
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(parsed_data)
        print(f"   Successfully wrote to {filename}")
        return f"Wrote to {filename}"
    except Exception as e:
        print(f"❌ CSV Write Error: {e}")
        return "Error"

def tool_send_email(to_address="", subject="", message=""):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not sender or not password:
        print("❌ ERROR: EMAIL_ADDRESS and EMAIL_PASSWORD must be in .env")
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
    print(f"🔔 Sending webhook message...")
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
    # Core Tools
    "print": tool_print,
    "create_file": tool_create_file,
    "read_file": tool_read_file,
    "parse_json": tool_parse_json,
    "open_url": tool_open_url,
    "calculate": tool_calculate,
    "think": tool_llm_think,
    "input": tool_input,
    
    # The 10 Autonomous Tools
    "get_time": tool_get_time,
    "random_number": tool_random_number,
    "run_terminal": tool_run_terminal,
    "scrape_webpage": tool_scrape_webpage,
    "fetch_api": tool_fetch_api,
    "download_file": tool_download_file,
    "read_csv": tool_read_csv,
    "write_csv": tool_write_csv,
    "send_email": tool_send_email,
    "send_webhook": tool_send_webhook
}

# ==========================================
# 3. THE LARK GRAMMAR
# ==========================================
grammar = r"""
    start: statement*
    
    ?statement: agent_cmd | model_cmd | use_llm_cmd | action_cmd | save_cmd 
              | list_cmd | if_cmd | loop_cmd | foreach_cmd | while_cmd

    agent_cmd: "Agent is" NAME
    model_cmd: "Model is" NAME
    use_llm_cmd: "Use LLM"
    action_cmd: "Action is" NAME (STRING)*
    save_cmd: "Save result as" NAME
    
    list_cmd: "Create list" NAME "with" STRING ("," STRING)*
    
    if_cmd: "If" NAME "is" STRING "then" block ("else" block)?
    loop_cmd: "Repeat" NUMBER "times" block
    foreach_cmd: "For each" NAME "in" NAME block
    while_cmd: "While" NAME "is" STRING block
    
    block: "{" statement* "}"
    
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
# 4. HELPER: Variable Interpolation
# ==========================================
def interpolate_variables(text, context):
    def replacer(match):
        var_name = match.group(1)
        if var_name in context:
            return str(context[var_name])
        else:
            print(f"⚠️  Warning: Variable '{{{var_name}}}' not found.")
            return match.group(0) 
    return re.sub(r'\{([a-zA-Z0-9_]+)\}', replacer, text)

# ==========================================
# 5. INTERPRETER: Execute a single block
# ==========================================
def execute_block(block_node, context, current_agent, current_model, use_llm):
    last_result = None
    for stmt in block_node.children:
        result = execute_statement(stmt, context, current_agent, current_model, use_llm)
        if result is not None:
            last_result = result
    return last_result

# ==========================================
# 6. INTERPRETER: Execute a statement
# ==========================================
def execute_statement(stmt, context, current_agent, current_model, use_llm):
    cmd_node = stmt
    cmd_type = cmd_node.data

    if cmd_type == "agent_cmd":
        context["_agent"] = cmd_node.children[0].value
        print(f"🤖 Loaded Agent: {context['_agent']}")

    elif cmd_type == "model_cmd":
        context["_model"] = cmd_node.children[0].value
        print(f"🧠 AI Model set to: {context['_model']}")
        
    elif cmd_type == "use_llm_cmd":
        context["_use_llm"] = True
        print("✨ LLM Mode Activated.")

    elif cmd_type == "list_cmd":
        var_name = cmd_node.children[0].value
        items = [str(s)[1:-1] for s in cmd_node.children[1:]]
        context[var_name] = items
        print(f"📋 Created list '{var_name}': {items}")
        return items

    elif cmd_type == "action_cmd":
        tool_name = cmd_node.children[0].value
        raw_args = [str(arg)[1:-1] for arg in cmd_node.children[1:]]
        args = [interpolate_variables(arg, context) for arg in raw_args]

        if tool_name in TOOLS:
            try:
                if tool_name == "think":
                    return TOOLS[tool_name](args[0] if args else "", context.get("_agent", "AI"), context.get("_model", "gpt-4o-mini"))
                elif len(args) == 1:
                    return TOOLS[tool_name](args[0])
                elif len(args) > 1:
                    return TOOLS[tool_name](*args)
                else:
                    return TOOLS[tool_name]()
            except Exception as e:
                print(f"❌ Tool Error ({tool_name}): {e}")
        else:
            if context.get("_use_llm"):
                print(f"⚠️ Tool '{tool_name}' not in toolbox. Routing to LLM...")
                return tool_llm_think(f"Execute: {tool_name} {' '.join(args)}", context.get("_agent", "AI"), context.get("_model", "gpt-4o-mini"))
            else:
                print(f"⚠️  Warning: Tool '{tool_name}' does not exist.")

    elif cmd_type == "save_cmd":
        var_name = cmd_node.children[0].value
        context[var_name] = context.get("_last_result", "None")
        print(f"💾 Saved to variable: {{{var_name}}}")

    elif cmd_type == "if_cmd":
        var_name = cmd_node.children[0].value
        expected_val = str(cmd_node.children[1])[1:-1]
        actual_val = str(context.get(var_name, ""))

        if actual_val == expected_val:
            print(f"✅ Condition met: {var_name} is '{expected_val}'")
            return execute_block(cmd_node.children[2], context, current_agent, current_model, use_llm)
        else:
            print(f"⏭️ Condition failed: {var_name} ('{actual_val}') is not '{expected_val}'")
            if len(cmd_node.children) > 3:
                return execute_block(cmd_node.children[3], context, current_agent, current_model, use_llm)

    elif cmd_type == "loop_cmd":
        times = int(cmd_node.children[0].value)
        print(f"🔁 Starting loop ({times} times)...")
        last_res = None
        for i in range(times):
            print(f"  🔄 Iteration {i+1}/{times}")
            last_res = execute_block(cmd_node.children[1], context, current_agent, current_model, use_llm)
        return last_res

    elif cmd_type == "foreach_cmd":
        item_var = cmd_node.children[0].value
        list_name = cmd_node.children[1].value
        block = cmd_node.children[2]
        
        if list_name in context and isinstance(context[list_name], list):
            items = context[list_name]
            print(f"🔁 Looping through list '{list_name}' ({len(items)} items)...")
            last_res = None
            for item in items:
                context[item_var] = item
                print(f"  🔄 Item: {item}")
                last_res = execute_block(block, context, current_agent, current_model, use_llm)
            return last_res
        else:
            print(f"❌ Error: '{list_name}' is not a valid list.")

    elif cmd_type == "while_cmd":
        var_name = cmd_node.children[0].value
        expected_val = str(cmd_node.children[1])[1:-1]
        block = cmd_node.children[2]
        
        iterations = 0
        last_res = None
        while str(context.get(var_name, "")) == expected_val and iterations < 100:
            print(f"  🔄 While loop running (Iteration {iterations+1})...")
            last_res = execute_block(block, context, current_agent, current_model, use_llm)
            iterations += 1
        return last_res

# ==========================================
# 7. MAIN ENGINE EXECUTION
# ==========================================
def run_bot_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {file_path}")
        return

    print(f"⚙️  Booting BotLang Engine V10...\n")

    try:
        parse_tree = parser.parse(code)
    except Exception as e:
        print(f"❌ SYNTAX ERROR:\n{e}")
        return

    context = {}
    
    for stmt in parse_tree.children:
        result = execute_statement(stmt, context, context.get("_agent"), context.get("_model"), context.get("_use_llm"))
        if result is not None:
            context["_last_result"] = result

    print("\n✅ Execution Finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine.py <your_file.bot>")
    else:
        run_bot_file(sys.argv[1])