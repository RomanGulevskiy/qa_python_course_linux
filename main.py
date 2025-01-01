from subprocess import run

from time import strftime


output = run("ps aux", shell=True, capture_output=True, text=True).stdout.splitlines()

data = {
    "users": {},
    "memory_usage": 0,
    "cpu_usage": 0,
    "max_memory": [],
    "max_cpu": []
}

for line in output[1:]:
    user = line.split()[0]
    memory = float(line.split()[3])
    cpu = float(line.split()[2])
    process = ' '.join(line.split()[10:])

    if user not in data["users"]:
        data["users"][user] = 1
    else:
        data["users"][user] += 1

    if not data["max_memory"]:
        data["max_memory"] = (memory, process)
    elif memory > data["max_memory"][0]:
        data["max_memory"] = (memory, process)

    if not data["max_cpu"]:
        data["max_cpu"] = (cpu, process)
    elif cpu > data["max_cpu"][0]:
        data["max_cpu"] = (cpu, process)

    data["memory_usage"] += memory
    data["cpu_usage"] += cpu

newline = "\n"

report = (
    f'Отчет о состоянии системы:\n'
    f'Пользователи системы: {", ".join(list(data["users"]))}\n'
    f'Процессов запущено: {len(output) - 1}\n\n'
    f'Пользовательских процессов запущено:\n'
    f'{newline.join(f"{key}: {value}" for key, value in list(data["users"].items()))}\n\n'
    f'Всего памяти используется: {data["memory_usage"]}%\n'
    f'Всего CPU используется: {data["cpu_usage"]}%\n'
    f'Больше всего памяти использует: {data["max_memory"][0]}% {data["max_memory"][1][:20]}\n'
    f'Больше всего CPU использует: {data["max_cpu"][0]}% {data["max_cpu"][1][:20]}'
)

current_datetime = strftime('%d-%m-%Y-%H:%M:%S')
with open(f'{current_datetime}-scan.txt', 'w', encoding='utf-8') as f:
    f.write(report)
