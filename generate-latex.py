import os
import codecs
import sys
from string import digits

reload(sys)
sys.setdefaultencoding("utf-8")

fout = codecs.open('bible.tex', 'w', encoding='utf-8')

def output(s):
    s1 = s.replace('_', '')
    fout.write(s1)
    fout.write('\n')

def parseChapter(book, chapter):
    chapterParts = chapter.split('_')
    output('\Chapter{' + chapterParts[1] + ' ' + chapterParts[2] + '}')
    with codecs.open(book + '/' + chapter, encoding='utf-8') as file:
        for line in file.readlines():
            if line[0] == '#':
                output('\Paragraph{' + line[2:] + '}')
            elif line[0].isdigit():
                output('\Verse{' + line.lstrip(digits).strip() + '}')
                

def parseBook(book):
    output('\Book{' + book.split('_')[1] + '}')
    chapters = sorted(list(filter(lambda dirname: dirname[0].isdigit(), os.listdir('./' + book))))
    for chapter in chapters:
        parseChapter(book, chapter)

def main(start, end):
    output('''
\\documentclass[a4paper]{ctexart}


\\title{CUV Bible}
\\date{\\today}

\\usepackage{zhfontcfg}

\\begin{document}
''')
    books = sorted(list(filter(lambda dirname: dirname[0].isdigit() and int(dirname[0:2]) >= int(start) and int(dirname[0:2]) < int(end), os.listdir('.'))))
    for book in books:
        parseBook(book)
    output('\\end{document}')

main(sys.argv[1], sys.argv[2])

