import pandas as pd
import numpy as np

def tag_wrap(wrapper, content):
    wrapper['left_tag'] = wrapper['left_tag'] + '\n'
    print(content[-1])
    if content[-1] != '\r' and content[-1] != '\n':
        wrapper['right_tag'] = '\n' + wrapper['right_tag']
    return wrapper['left_tag'] + content + wrapper['right_tag']

def df_to_html_table (df):
    table_header_wrap = {'left_tag':'<thead><tr class="row100 head">', 'right_tag' : '</tr></thead>'}
    table_item_row_wrap = {'left_tag':'<tr class="row100">', 'right_tag' : '</tr>'}
    table_item_list_wrap = {'left_tag':'<tbody>', 'right_tag' : '</tbody>'}

    header_line_wrap = {'left_tag':'<th class="column100 column{0[0]}" data-column="column{0[1]}">', 'right_tag':'</th>'}
    item_line_wrap = {'left_tag':'<td class="column100 column{0[0]}" data-column="column{0[1]}">', 'right_tag':'</td>'}

#make head
    header_content = ''
    item_content_one_row = ''
    item_content_list = ''

    for idx, val in enumerate(df.columns):
        args = (idx + 1, idx + 1)
        header_content_item_one_value = header_line_wrap['left_tag'].format(args) + str(val) +  header_line_wrap['right_tag'] + '\n'
        header_content = header_content + header_content_item_one_value

    header_content = tag_wrap(table_header_wrap, header_content)

# fill the content in the table item
    for index, row in df.iterrows():
        item_content_one_row = ''
        for index2, item in enumerate(row):
            args = (index2 + 1, index2 + 1)
            item_content_one_value = item_line_wrap['left_tag'].format(args) + str(item) +  item_line_wrap['right_tag'] + '\n'
            item_content_one_row = item_content_one_row + item_content_one_value
        item_content_list = item_content_list + tag_wrap(table_item_row_wrap, item_content_one_row)

    item_content = tag_wrap(table_item_list_wrap, item_content_list)

    html_table_content = header_content + item_content

    return html_table_content
