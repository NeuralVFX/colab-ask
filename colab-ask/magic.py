import io
import os
import re
import base64

# Third-party imports
import mistune
from PIL import Image
from IPython import get_ipython
from IPython.core.magic import register_cell_magic, register_line_magic
from IPython.display import HTML, Markdown, display

# Colab imports
from google.colab import _message, userdata

# LLM imports
import litellm
from litellm import ModelResponse, ModelResponseStream
from lisette import Chat

# Configuration
litellm.drop_params = True


HEADER_HTML = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-c.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-java.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script>Prism.highlightAll();</script>
"""

def prep_markdown_cell(markdown_cell):
    """
    Extracts text and embedded images from a markdown cell.

    Args:
        markdown_cell (dict): The JSON dictionary representing a markdown cell.

    Returns:
        list: A list containing strings (text content) and bytes (decoded image data).
    """
    output_list = ['## Markdown Cell\n']

    for block in markdown_cell['source']:
        if "(data:image/" in block:
            base_64_text = block.split('base64,')[1]
            base_64_text = base_64_text.split(')')[0]
            output_image_bytes =  base64.b64decode(base_64_text)
            output_list.append(output_image_bytes )
 
        else:
            output_list.append(block)
    return output_list
    

def get_above_cells(cell_list, magic_input):
    """
    Filters the notebook cells to return only those preceding the current execution.

    Args:
        cell_list (list): Full list of cells from the notebook JSON.
        magic_input (str): The content of the current cell.

    Returns:
        list: A list of cell dictionaries that appear before the current cell.
    """
    cells_above_command = []

    ip = get_ipython()
    parent_header = ip.parent_header


    colab_meta = parent_header['metadata']['colab']
    cell_id = colab_meta['cell_id']

    for cell in cell_list:
        if cell['metadata']['id'] == cell_id:
            break
        else:
            cells_above_command.append(cell)
    return cells_above_command


def format_for_chat(items):
    """
    Formats a list of mixed text and image bytes into the OpenAI/LiteLLM message structure.

    Args:
        items (list): A list containing strings or byte objects.

    Returns:
        list: A list of dictionaries with 'type' (text/image_url) keys.
    """
    formatted = []
    
    for item in items:
        if isinstance(item,str):
            if item != '':
                formatted.append( {"type": "text", "text": item})
        elif isinstance(item,bytes):
            img = Image.open(io.BytesIO(item))
            img_format = img.format.lower()
            base64_string = base64.b64encode(item).decode('utf-8')
            formatted.append( {"type": "image_url", "image_url": {"url": f"data:image/{img_format};base64,{base64_string}"}})
    
    return formatted


def prep_code_cell(code_cell,cell_type='Code'):
    """
    Extracts and labels source code from a code cell.

    Args:
        code_cell (dict): The JSON dictionary representing a code cell.
        cell_type (str, optional): Label for the cell. Defaults to 'Code'.

    Returns:
        list: A list containing the labeled header and the source code string.
    """
    output_list = [f'{cell_type} Cell\n']

    code_input = ''.join(code_cell['source'])
    output_list.append(code_input)

    return output_list


def prep_code_cell_output(code_cell,cell_type='Code'):
    """
    Extracts outputs (logs, streams, errors, images) from a code cell.

    Args:
        code_cell (dict): The JSON dictionary representing a code cell.
        cell_type (str, optional): Label for the cell. Defaults to 'Code'.

    Returns:
        list: A list containing text output, error traces, or image bytes.
    """
    if cell_type == 'Code':
        output_list = ['### Code Cell Output\n']
    else:
        output_list = []
        
    for block in code_cell['outputs']:

        if block['output_type'] == 'display_data':
            image_keys = [key for key in block['data'].keys() if 'image' in key]
            for key in  block['data'].keys():
                if 'image' in key:
                    base_64_text = block['data'][key]
                    output_image_bytes = base64.b64decode(base_64_text)
                    output_list.append(output_image_bytes)
                if 'text' in key:
                    output_list.append(block['data'][key])


        elif block['output_type'] == 'stream':
            output_list.append(''.join(block['text']))

        elif block['output_type'] == 'error' :
            output_list.append('#### Error\n')  
            output_list.append(f'evalue:{block['evalue']}\n\n traceback:{block['traceback']}')  

    return output_list


def is_ask_cell(cell):
    """
    Checks if a cell contains the %%ask magic command.

    Args:
        cell (dict): The cell dictionary.

    Returns:
        bool: True if it is an %%ask cell, False otherwise.
    """
    answer = False
    if len(cell['source']) > 1:
        if cell['source'][0] == '%%ask\n':
            answer = True
    return answer


def preprare_chat_history(cell_list):
    """
    Converts a list of notebook cells into a conversation history for the LLM.

    Args:
        cell_list (list): List of notebook cells.

    Returns:
        list: A list of message dictionaries (role/content) for the Chat API.
    """
    cell_context = []
    for cell in cell_list:
        cell_type = cell['cell_type']

        if cell_type == 'markdown':

            formatted = format_for_chat(prep_markdown_cell(cell))
            if formatted:

                cell_context.append( {"role": "user", "content": formatted} )

        elif cell_type == 'code':

            sub_type = 'Code'
            response_role = 'user'

            if is_ask_cell(cell):
                sub_type = 'User Question'
                response_role = 'assistant'

            formatted = format_for_chat(prep_code_cell(cell,cell_type=sub_type))
            if formatted:
                cell_context.append( {"role": "user", "content": formatted} )

            formatted = format_for_chat(prep_code_cell_output(cell,cell_type=sub_type))
            if formatted:
                cell_context.append( {"role": response_role, "content":formatted} )
    return cell_context
    

def ask(line, cell):
    """
    The %%ask cell magic handler.
    """
    # Get notebook JSON
    notebook_json = _message.blocking_request('get_ipynb')

    # Your existing function
    response = ask_llm(notebook_json, cell)


def set_model(line):
    """
    Magic command (%set_model) to change the active LLM.
    """
    os.environ['ASK_MODEL'] = line.strip()
    print(f"Model set to: {line.strip()}")


def set_sys(line, cell):
    """
    Magic command (%%set_sys) to update the system prompt.
    """
    os.environ['ASK_SYSTEM_PROMPT'] = cell.strip()
    print(f"System prompt updated")
    

def ask_llm(json_data, magic_input):
    """
    Orchestrates the LLM interaction.

    Args:
        json_data (dict): The full notebook JSON structure.
        magic_input (str): The user's query from the %%ask cell.
    """
    system_prompt = os.environ['ASK_SYSTEM_PROMPT']

    cell_list = json_data['ipynb']['cells']
    cell_list = get_above_cells(cell_list,magic_input)
    chat_history = preprare_chat_history(cell_list)

    chat = Chat(model=os.environ['ASK_MODEL'],
                            cache=False,
                            hist=chat_history,
                            sp=system_prompt)

    chat_input = f'USER REQUEST (Current Cell):  {magic_input}\n'

    res_gen = chat(chat_input,stream=True)
    display_handle = display(Markdown(""), display_id=True)
    
    display(HTML(HEADER_HTML))

    accumulated_text = ""

    for chunk in res_gen:
        if isinstance(chunk,ModelResponseStream):
            if chunk.choices[0].delta.content:
              accumulated_text += chunk.choices[0].delta.content
              html_output = mistune.html(accumulated_text)
              display_handle.update(HTML(html_output+'<script>Prism.highlightAll()</script>'))
              

def load_ipython_extension(ipython):
    """
    Extension entry point. Called when %load_ext colab_ask is run.
    """
    from google.colab import userdata
    
    llm_key_names = ['OPENAI_API_KEY','ANTHROPIC_API_KEY','GEMINI_API_KEY']
    for key_name in llm_key_names:
        try: os.environ[key_name] = userdata.get(key_name); print(f'Set Env Key For: {key_name}')
        except: pass

    if 'ASK_MODEL' not in os.environ: os.environ['ASK_MODEL'] = 'claude-sonnet-4-5-20250929'

    sys_prompt =( "You are an AI assistant inside a Google Colab notebook.\n"
                "In your response, craft guidance on the next step, whether code related, or more strategy related \n"
                "Dont spew out all the steps at once, the user wants to go slow, they will ask for more if they need it \n"
                "The user is interested in improving there coding, and may chose to make code blocks in repsonse to your input \n")

    if 'ASK_SYSTEM_PROMPT' not in os.environ: os.environ['ASK_SYSTEM_PROMPT'] = sys_prompt
    ipython.register_magic_function(ask, 'cell')
    ipython.register_magic_function(set_model, 'line')
    ipython.register_magic_function(set_sys, 'cell')
