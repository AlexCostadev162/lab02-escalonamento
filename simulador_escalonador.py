import copy


class Processo:
    def __init__(self, pid, chegada, duracao):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.restante = duracao
        self.finalizacao = 0
        self.espera = 0
        self.retorno = 0


def mostrar_gantt(execucoes):
    print("\nDiagrama de Gantt:")

    linha = ""
    tempos = ""

    for pid, inicio, fim in execucoes:
        bloco = f"| {pid} "
        linha += bloco
        tempos += f"{inicio:<{len(bloco)}}"

    linha += "|"
    tempos += str(execucoes[-1][2])

    print(linha)
    print(tempos)


def simular_fcfs(processos):
    procs = copy.deepcopy(processos)
    procs = sorted(procs, key=lambda x: x.chegada)

    tempo_atual = 0
    execucoes = []

    print("\n" + "=" * 55)
    print("SIMULACAO FCFS")
    print("=" * 55)

    for p in procs:
        if tempo_atual < p.chegada:
            tempo_atual = p.chegada

        inicio = tempo_atual
        tempo_atual += p.duracao

        p.finalizacao = tempo_atual
        p.retorno = p.finalizacao - p.chegada
        p.espera = p.retorno - p.duracao

        execucoes.append((p.pid, inicio, p.finalizacao))

        print(
            f"Processo {p.pid}: "
            f"Fim={p.finalizacao} ms | "
            f"Espera={p.espera} ms | "
            f"Retorno={p.retorno} ms"
        )

    media_espera = sum(p.espera for p in procs) / len(procs)
    media_retorno = sum(p.retorno for p in procs) / len(procs)

    mostrar_gantt(execucoes)

    print(f"\nTempo Medio de Espera:  {media_espera:.2f} ms")
    print(f"Tempo Medio de Retorno: {media_retorno:.2f} ms")

    return procs


def simular_round_robin(processos, quantum=3):
    procs = copy.deepcopy(processos)

    tempo_atual = 0
    fila = []
    concluidos = []
    execucoes = []

    procs_ord = sorted(procs, key=lambda x: x.chegada)
    adicionados = set()

    def adicionar_fila(tempo):
        for i, p in enumerate(procs_ord):
            if p.chegada <= tempo and i not in adicionados:
                fila.append(p)
                adicionados.add(i)

    adicionar_fila(tempo_atual)

    print("\n" + "=" * 55)
    print(f"ROUND ROBIN - QUANTUM = {quantum} ms")
    print("=" * 55)

    while fila:
        p_atual = fila.pop(0)

        inicio = tempo_atual
        tempo_execucao = min(p_atual.restante, quantum)

        tempo_atual += tempo_execucao
        p_atual.restante -= tempo_execucao

        execucoes.append((p_atual.pid, inicio, tempo_atual))

        adicionar_fila(tempo_atual)

        if p_atual.restante > 0:
            fila.append(p_atual)
        else:
            p_atual.finalizacao = tempo_atual
            p_atual.retorno = p_atual.finalizacao - p_atual.chegada
            p_atual.espera = p_atual.retorno - p_atual.duracao
            concluidos.append(p_atual)

    concluidos = sorted(concluidos, key=lambda x: x.pid)

    for p in concluidos:
        print(
            f"Processo {p.pid}: "
            f"Fim={p.finalizacao} ms | "
            f"Espera={p.espera} ms | "
            f"Retorno={p.retorno} ms"
        )

    mostrar_gantt(execucoes)

    media_espera = sum(p.espera for p in concluidos) / len(concluidos)
    media_retorno = sum(p.retorno for p in concluidos) / len(concluidos)

    trocas = 0
    for i in range(1, len(execucoes)):
        if execucoes[i][0] != execucoes[i - 1][0]:
            trocas += 1

    print(f"\nFatias de CPU executadas: {len(execucoes)}")
    print(f"Trocas de contexto:       {trocas}")
    print(f"Tempo Medio de Espera:  {media_espera:.2f} ms")
    print(f"Tempo Medio de Retorno: {media_retorno:.2f} ms")

    return concluidos


if __name__ == "__main__":
    workload = [
        Processo("P1", 0, 8),
        Processo("P2", 1, 4),
        Processo("P3", 2, 9),
        Processo("P4", 3, 5)
    ]

    print("\nSIMULADOR DE ESCALONAMENTO DE CPU")
    print("\nCarga de trabalho:")
    print("Processo | Chegada | Duracao")
    print("----------------------------")

    for p in workload:
        print(
            f"{p.pid:^8} | "
            f"{p.chegada:^7} | "
            f"{p.duracao:^7}"
        )

    simular_fcfs(workload)
    simular_round_robin(workload, quantum=3)
    simular_round_robin(workload, quantum=1)
    simular_round_robin(workload, quantum=50)
