from typing import List, Iterable


def get_process_info_lines(port: int) -> List[str]:
    from subprocess import Popen, PIPE

    process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    return str(stdout.decode("utf-8")).split("\n")[1:]


def split_process_line(process: str) -> List[str]:
    return [x for x in process.split(" ") if x != '']


def extract_pids(lines: List[str]) -> Iterable[str]:
    for process in lines:
        splited_line = split_process_line(process)
        if len(splited_line) < 2:
            continue
        try:
            yield int(splited_line[1])
        except ValueError:
            continue


def kill_process(pid: int):
    from os import kill
    from signal import SIGKILL
    return kill(pid, SIGKILL)


def main(arguments: List[str]) -> None:
    if len(arguments) < 2:
        raise Exception('Invalid set of arguments.')

    port = int(arguments[1])
    lines = get_process_info_lines(port)

    if not lines:
        raise Exception(f'No process with port : [{port}] found.')

    pids = extract_pids(lines)
    pid_to_kill = next(pids, None)

    if not pid_to_kill:
        raise Exception('PID was not found.')

    kill_process(pid_to_kill)


if __name__ == '__main__':
    from sys import argv
    main(argv)
