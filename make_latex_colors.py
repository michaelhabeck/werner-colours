"""
Colors from Nicholas Rougeux's spreadsheet

https://docs.google.com/spreadsheets/d/10w7UebIDqN6ChEpBwLDQmAgVZZhLtKvnrLeNnBjJmsc/edit#gid=0
"""
import os
import string
import numpy as np

from collections import OrderedDict

TEST_LINE = '\\noindent\\textcolor{{{0}}}{{\\textbf{{{1}}}}}\\\\'
TEST_LINE = '\\noindent\\colorbox{{{0}}}{{\\textcolor{{{2}}}{{\\textbf{{{1}}}}}}}\\\\'
TEST_LINE = '\\noindent\\colorbox{{{0}}}{{\\textcolor{{{2}}}{{{{{1}}}}}}}\\\\'
TEST_LINE = '\\noindent\\fcolorbox{{{2}}}{{{0}}}{{\\textcolor{{{2}}}{{{{{1}}}}}}}\\hfill{{\\footnotesize {0}}}\\\\'

TEST = ['\\documentclass[a4paper,12pt]{article}',
        '\\usepackage{geometry}',
        '\\geometry{a4paper}',
        '\\setlength{\\parindent}{0cm}',
        '\\usepackage{xcolor}',
        '\\input{wernercolors}',
        '\\begin{document}',
        '\\Large',
        '\\end{document}']

class Color(object):

    latex_string = '\\definecolor{{{0}}}{{HTML}}{{{1}}}'

    def __init__(self, properties):
        self.properties = properties

    @property
    def latex_name(self):
        return self.properties['Name'].replace(' ','')

    @property
    def hex_code(self):
        return self.properties['Hex'].lstrip('#').upper()

    @property
    def luminance(self):
        return luminance(hex2rgb(self.hex_code))

    @property
    def latex(self):
        return self.__class__.latex_string.format(
            self.latex_name, self.hex_code)

def random_line(n_chr=60):
    chrs = list(string.uppercase) + list(string.lowercase) + [' ', '; ', ', ']
    return ''.join([chrs[i] for i in np.random.randint(0,len(chrs),n_chr)])

def hex2rgb(hex_code):
    return tuple(int(hex_code[i:i+2],16) for i in (0,2,4))

def luminance(rgb):
    R, G, B = rgb
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def read_colors(tsvfile='Werner\'s Nomenclature of Colours - Colors.tsv'):

    rows = open(tsvfile).readlines()
    rows = [row.split('\t') for row in rows]

    header = rows.pop(0)
    colors = []

    for row in rows:
        properties = dict(zip(header, row))
        colors.append(Color(properties))

    return colors

def write_colors(colors, filename='./wernercolors.tex'):

    with open(filename,'w') as fh:
        for color in colors:
            fh.write(color.latex + '\n')

def make_testfile(colors, filename='./test.tex', luminance_threshold=(120,150)[0], sans=False):

    text_line = random_line(40)
    text_line = 'Von drauss\' vom Walde komm ich her; ich muss euch sagen, es weihnachtet sehr!'
    text_line = text_line[:35]

    if sans:
        text_line = '\\sffamily{{{0}}}'.format(text_line)

    with open(filename,'w') as fh:

        for color in colors[:]:

            text_color = 'white' if color.luminance < luminance_threshold else 'black'

            TEST.insert(-1,TEST_LINE.format(
                color.latex_name,
                text_line, 
                text_color))

        fh.write('\n'.join(TEST))

    output = os.popen('pdflatex ./test.tex').read()

    return output

if __name__ == '__main__':

    colors = read_colors()
    write_colors(colors)
    make_testfile(colors)
