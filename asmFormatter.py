import pyperclip
from time import sleep
import sys

false = False
true = True
SPACES_TO_COMM = 2
SPACES_FROM_DOT_TO_COMM = 1
SPACES_TO_COMM_LINKS = 0
SPACES_FROM_DOT_TO_COMM_LINKS = 1
IS_CHANGE_SPACES_FROM_DOT_TO_COMM = False
IS_SPLIT_FOR_BLANK_LINE = True
IGNORE_LINER_GREATER = 150
SEPARATOR_SYMBOL = ";"
LINK_SYMBOL = ":"
REFORMAT_LINKS = True

READ_FROM_BUFFER = False


def pre_complete_block(data: list[str], separator=LINK_SYMBOL, spaces_to_comm=SPACES_TO_COMM_LINKS,
                       spaces_from_dot_to_comm=SPACES_FROM_DOT_TO_COMM_LINKS) -> list[str]:
    max_len = 0
    for q in data:
        if q == "" or q.find(separator) == -1:
            continue
        max_len = max(q.find(separator), max_len)
    for w in range(len(data)):
        if data[w].find(separator) == -1:
            q = separator + data[w]
        else:
            q = data[w]
        if len(q) > IGNORE_LINER_GREATER or q.find(separator) == -1:
            continue
        data[w] = (q[:q.find(separator)] + " " * spaces_to_comm + separator + " " * (max_len - q.find(separator)) +
                   " " * spaces_from_dot_to_comm + q[q.find(separator):][1:].strip())
        if data[w][0] == separator:
            data[w] = " " + data[w][1:]
    return data


def complete_block(data: list[str], separator=SEPARATOR_SYMBOL, spaces_to_comm=SPACES_TO_COMM,
                   spaces_from_dot_to_comm=SPACES_FROM_DOT_TO_COMM) -> list[str]:
    max_len = 0
    for q in data:
        if q == "" or len(q) > IGNORE_LINER_GREATER or q.find(separator) == -1:
            continue
        max_len = max(len(q[:q.find(separator)].rstrip()), max_len)
    for w in range(len(data)):
        q = data[w]
        if len(q) > IGNORE_LINER_GREATER or q.find(separator) == -1:
            continue
        data[w] = (q[:q.find(separator)].rstrip() + " " * (
                max_len - len(q[:q.find(separator)].rstrip()) + spaces_to_comm) +
                   separator + " " * spaces_from_dot_to_comm + q[q.find(separator):][1:].strip())
    return data


def get_blocks(data: str) -> list[str]:
    buf = []
    for q in data.split("\n"):
        curr = q.strip()
        if curr != "":
            if len(buf) > 1 and buf[-1] == "":
                if IS_SPLIT_FOR_BLANK_LINE:
                    yield buf
                    buf = []
        buf.append(curr)
    yield buf


def formate_code(data: str) -> str:
    formatted_code = ""
    for q in get_blocks(data):
        formatted_code += "\n".join(complete_block(pre_complete_block(q) if REFORMAT_LINKS else q)) + "\n"
    formatted_code = formatted_code[:-1]
    return formatted_code


def main():
    try:
        if READ_FROM_BUFFER:
            pyperclip.copy(formate_code(pyperclip.paste()))
            print("Успешно!")
            sleep(0.3)
        else:
            sys.stdout.write(formate_code(sys.stdin.read()))
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Выход через 10 секунд...")
        sleep(10)


main()
