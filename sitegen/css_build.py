"""Conservative production CSS minification; source CSS stays readable."""
import re


def minify(text):
    parts = re.split(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/)', text, flags=re.S)
    output = []
    for part in parts:
        if not part or part.startswith('/*'):
            continue
        if part.startswith(('"', "'")):
            output.append(part)
        else:
            value = re.sub(r'\s+', ' ', part)
            value = re.sub(r'\s*([{};])\s*', r'\1', value)
            output.append(value)
    return ''.join(output).strip() + '\n'
