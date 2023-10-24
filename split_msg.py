import click

from msg_split import split_message, MAX_LEN


@click.command()
@click.option('--max-len', default=MAX_LEN, type=int, help='Maximum length of the message fragment')
@click.argument('file_path', type=click.Path(exists=True, readable=True))
def main(max_len: int, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for fragment in split_message(content, max_len):
        print(fragment)
        print("<hr>")

if __name__ == "__main__":
    main()
