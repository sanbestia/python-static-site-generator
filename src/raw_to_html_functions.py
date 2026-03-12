def raw_to_html_paragraph(text):
    return f"<p>{text.replace('\n', ' ')}</p>"

def raw_to_html_heading(text, level):
    if level < 1 or level > 6:
        raise ValueError('Heading level must be between 1 and 6')
    return f'<h{level}>{text}</h{level}>'

def raw_to_html_bold(text):
    return f'<strong>{text}</strong>'

def raw_to_html_italic(text):
    return f'<em>{text}</em>'

def raw_to_html_link(text, link):
    return f'<a href="{link}">{text}</a>'

def raw_to_html_image(text, link):
    return f'<img src="{link}" alt="{text}">'

def raw_to_html_unordered_list(inner_text):
    return f'<ul>\n{inner_text}</ul>'

def raw_to_html_ordered_list(inner_text):
    return f'<ol>\n{inner_text}</ol>'

def raw_to_html_list_element(text):
    return f'<li>{text}</li>\n'

def raw_to_html_quote(inner_text):
    return f'<blockquote>{inner_text}</blockquote>'
    
def raw_to_html_code_oneliner(inner_text):
    return f'<code>{inner_text}</code>'

def raw_to_html_codeblock(inner_text):
    return f'<pre><code>{inner_text}</code></pre>'

def raw_to_html_div(inner_text):
    return f'<div>{inner_text}</div>'

def raw_to_html_span(inner_text):
    return f'<span>{inner_text}</span>'
