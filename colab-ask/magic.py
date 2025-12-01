import os
from IPython.core.magic import register_cell_magic, register_line_magic
from IPython.display import Markdown, display, HTML
from lisette import Chat
import base64
from google.colab import userdata
from google.colab import _message
import litellm
from litellm import ModelResponse, ModelResponseStream
from PIL import Image
import io
import mistune
import re
from mistune import create_markdown

litellm.drop_params = True


header_html = """
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
    output_list = [f'{cell_type} Cell\n']

    code_input = ''.join(code_cell['source'])
    output_list.append(code_input)

    return output_list


def prep_code_cell_output(code_cell,cell_type='Code'):

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
    answer = False
    if len(cell['source']) > 1:
        if cell['source'][0] == '%%ask\n':
            answer = True
    return answer


def preprare_chat_history(cell_list):
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
    

def ask_llm(json_data, magic_input):

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
    
    display(HTML(header_html))

    accumulated_text = ""

    for chunk in res_gen:
        if isinstance(chunk,ModelResponseStream):
            if chunk.choices[0].delta.content:
              accumulated_text += chunk.choices[0].delta.content
              html_output = mistune.html(accumulated_text)
              display_handle.update(HTML(html_output+'<script>Prism.highlightAll()</script>'))
              

def ask(line, cell):
    # Get notebook JSON
    notebook_json = _message.blocking_request('get_ipynb')

    # Your existing function
    response = ask_llm(notebook_json, cell)
   

def set_model(line):
    os.environ['ASK_MODEL'] = line.strip()
    print(f"Model set to: {line.strip()}")


def set_sys(line, cell):
    os.environ['ASK_SYSTEM_PROMPT'] = cell.strip()
    print(f"System prompt updated")
    

def load_ipython_extension(ipython):
    from google.colab import userdata
    
    llm_key_names = ['OPENAI_API_KEY','ANTHROPIC_API_KEY','GEMINI_API_KEY']
    for key_name in llm_key_names:
        try: os.environ[key_name] = userdata.get(key_name); print(f'Set Env Key For: {key_name}')
        except: pass

    if 'ASK_MODEL' not in os.environ: os.environ['ASK_MODEL'] = 'claude-sonnet-4-5-20250929'

    sys_prompt =( "You are an AI assistant inside a Google Colab notebook.\n"
                "In your response, craft guidance on the next step, whether code related, or more strategy related. \n"
                "Dont spew out all the steps at once, the user wants to go slow, they will ask for more if they need it. \n"
                "The user is interested in improving there coding, and may chose to make code blocks in repsonse to your input. \n"
                "If the user doesnt finish a scentence, you are meant to respond, not complete there phrase.")

    if 'ASK_SYSTEM_PROMPT' not in os.environ: os.environ['ASK_SYSTEM_PROMPT'] = sys_prompt
    ipython.register_magic_function(ask, 'cell')
    ipython.register_magic_function(set_model, 'line')
    ipython.register_magic_function(set_sys, 'cell')
