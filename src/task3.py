import glob

def convert_to_markdown_table(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Split lines into header and data
    header = lines[0].strip().split('\t')
    data = [line.strip().split('\t') for line in lines[1:]]

    # Create the markdown table
    markdown_table = '| ' + ' | '.join(header) + ' |\n'
    markdown_table += '| ' + ' | '.join(['---'] * len(header)) + ' |\n'

    for row in data:
        markdown_table += '| ' + ' | '.join(row) + ' |\n'

    return markdown_table

def save_markdown_table(markdown_table, file_path):
    with open(file_path, 'w') as file:
        file.write(markdown_table)


def task1_md():
    file_path = '../solutions/task1.txt'
    markdown_table = convert_to_markdown_table(file_path)
    save_markdown_table(markdown_table, './solutions/task1.md')


def task2_md():
    superheroes_path='./solutions/task2/*.txt'
    output_path='./solutions/task3/'
    superhero_files=glob.glob(superheroes_path)
    for file_path in superhero_files:
        md=convert_to_markdown_table(file_path)
        save_markdown_table(md, f'{output_path}/{file_path.split("/")[-1].split(".txt")[0]}.md')


def main():
    task1_md()
    task2_md()

if __name__ == '__main__':  
    main()

