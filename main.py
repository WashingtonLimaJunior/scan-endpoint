import subprocess
import re

def get_netstat_output():
    # Executa o comando netstat para capturar todas as conexões abertas
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
    return result.stdout

def parse_netstat_output(output):
    # Expressão regular para capturar os detalhes relevantes da saída do netstat
    pattern = re.compile(r'\s*(TCP|UDP)\s+(\S+:\d+)\s+(\S+:\d+)\s+(LISTENING|ESTABLISHED|CLOSE_WAIT|SYN_SENT|SYN_RECEIVED|FIN_WAIT1|FIN_WAIT2|TIME_WAIT|CLOSED|UNKNOWN)\s+(\d+)\s*')
    connections = []

    for line in output.splitlines():
        match = pattern.match(line)
        if match:
            proto, local_addr, remote_addr, status, pid = match.groups()
            connections.append((proto, local_addr, remote_addr, status, pid))
    
    return connections

def get_process_name(pid):
    try:
        # Executa o comando tasklist para obter o nome do processo baseado no PID
        result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], capture_output=True, text=True)
        output = result.stdout.splitlines()

        # Itera sobre a saída do tasklist para capturar o nome do processo
        for line in output:
            if line.startswith("=======") or len(line.strip()) == 0:
                continue
            if str(pid) in line:
                return line.split()[0]  # Nome do processo é o primeiro item da linha
    except Exception as e:
        print(f"Error fetching process name for PID {pid}: {e}")
    
    return "Unknown"

def main():
    # Captura a saída do netstat
    netstat_output = get_netstat_output()
    
    # Debug: imprimir a saída completa do netstat para verificar
    print("Netstat Output:\n")
    print(netstat_output)

    # Processa a saída do netstat
    connections = parse_netstat_output(netstat_output)

    # Exibe os resultados em um formato tabular
    print("\nLocal Address         Remote Address        Status       PID   Process Name")
    for proto, local_addr, remote_addr, status, pid in connections:
        process_name = get_process_name(pid)
        print(f"{local_addr:<20} {remote_addr:<20} {status:<12} {pid:<5} {process_name}")

if __name__ == "__main__":
    main()
