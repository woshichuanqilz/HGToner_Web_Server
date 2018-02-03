import re
import ast
with open('page_content.txt') as the_file:
    page_content_dict = ast.literal_eval(the_file.read())

def render_render_template (dict_content, dict_var_name):
    cmd = "render_template(html_template_path, "
    for key, value in dict_content.items():
        cmd = cmd + key + ' = '+ dict_var_name + '[\'' + key + '\']' + ', '
    temp = ''
    cmd = re.sub(r",\s*$", "", cmd) + ')'
    print('-' * 20)
    print(cmd)
    print('-' * 20)

render_render_template(page_content_dict, 'page_content_dict')
