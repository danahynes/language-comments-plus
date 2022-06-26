#!/usr/bin/env python3

import json
import re

def main():
    JSON = 1

    tokens = []

    if JSON == 1:

        with open('tokens.json') as file:
            jlist = json.load(file)

        for item in jlist:

            name = ''
            color = ''
            background_color = ''
            font_weight = ''
            if 'name' in item:
                name = item['name']
            if 'color' in item:
                color = item['color']
            if 'background-color' in item:
                background_color = item['background-color']
            if 'font-weight' in item:
                font_weight = item['font-weight']
            token = {
                'name' : name,
                'color': color,
                'background-color': background_color,
                'font-weight': font_weight
            }

            tokens.append(token)

    else:

        with open('tokens.txt') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split('|')

            token = {
                'name': parts[0],
                'color': parts[1],
                'background-color': parts[2],
                'font-weight': parts[3]}
            tokens.append(token)

    # ------------------------------------------------------------------------------

    tokenstr = ''
    for token in tokens:
        tokenstr += ('|' + token['name'])
    tokenstr = tokenstr[1:]

    out =  'scopeName: \'text.comments-plus\'\n'
    out += 'injectionSelector: \'comment\'\n'
    out += 'patterns: [\n'
    out += '  {\n'
    out += '    match: \'\\\\b(' + tokenstr + ')\\\\b\'\n'
    out += '    name: \'comment.$1.comments-plus\'\n'
    out += '  }\n'
    out += ']\n'

    with open('grammars.cson', 'w') as file:
        file.write(out)

    # ------------------------------------------------------------------------------

    out = 'atom-text-editor {\n'

    for token in tokens:
        out += ('  .syntax--' + token['name'] + '.syntax--todos {\n')
        if token['color'] != '':
            out += ('    color: ' +  token['color'] + ';\n')
        if token['background-color'] != '':
            out += ('    background-color: ' +  token['background-color'] + ';\n')
        if token['font-weight'] != '':
            out += ('    font-weight: ' +  token['font-weight'] + ';\n')
        out += '  }\n'

    out += '}'

    with open('styles.less', 'w') as file:
        file.write(out)

    # ------------------------------------------------------------------------------

    snippets = {}

    if JSON == 1:

        with open('snippets.json') as file:
            snippets = json.load(file)

        # for key in list:
        #     snippets[key] = list[key]

    else:

        with open('snippets.txt') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split('|')
            snippets[parts[0]] = parts[1]

    out = ''
    for lang in snippets:
        out += '\'' + lang + '\':\n'
        for token in tokens:
            out += '  \'' + token['name'] + ' Comment\':\n'
            out += '    prefix: \'' + token['name'].lower() + '\'\n'
            out += '    body: \'' + snippets[lang] + '\'\n'

    with open('snippets.cson', 'w') as file:
        file.write(out)

if __name__ == '__main__':
    main()
