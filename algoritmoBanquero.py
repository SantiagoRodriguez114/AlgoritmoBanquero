import random

# Recursos
TOTAL = [20, 50, 30]

PROCESOS = ["P1", "P2", "P3", "P4"]

# Demanda máxima
MAX = [
    [10, 25, 0],  # P1
    [10, 25, 0],  # P2
    [10, 0, 15],  # P3
    [10, 0, 15],  # P4
]

# Duración en ciclos
DUR = [3, 3, 2, 2]

alloc = [[0]*3 for _ in range(4)]
need  = [row[:] for row in MAX]
rest  = [None]*4
done  = [False]*4

minuto = 0
fase = 0  # 0 = horizontal, 1 = vertical



# BANQUERO
def available():
    return [TOTAL[j] - sum(alloc[i][j] for i in range(4)) for j in range(3)]

def es_seguro():
    work = available()
    finish = [False]*4

    while True:
        progreso = False
        for i in range(4):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(3)):
                for j in range(3):
                    work[j] += alloc[i][j]
                finish[i] = True
                progreso = True
        if not progreso:
            break

    return all(finish)



# SEMAFORO
def procesos_activos():
    return [0,1] if fase == 0 else [2,3]

def nombre_fase():
    return "HORIZONTAL" if fase == 0 else "VERTICAL"

def semaforo(i):
    if done[i]: return "OFF"
    if i not in procesos_activos(): return "ROJO"
    if rest[i] is None: return "AMARILLO"
    return "VERDE"


# SIMULACION
while not all(done):
    minuto += 5
    print(f"\n── Minuto {minuto} ({nombre_fase()}) ─────────────")
    print("  " + "  ".join(f"{PROCESOS[i]}:{semaforo(i)}" for i in range(4)))
    print(f"  Disponible: {available()}")

    # avanzar
    for i in range(4):
        if rest[i] is not None and not done[i]:
            rest[i] -= 1
            if rest[i] == 0:
                alloc[i] = [0,0,0]
                done[i] = True
                print(f"  {PROCESOS[i]} COMPLETO — libera recursos")

    # entrada
    for i in random.sample(procesos_activos(), len(procesos_activos())):
        if done[i] or rest[i] is not None:
            continue

        req = need[i][:]
        av  = available()

        if any(req[j] > av[j] for j in range(3)):
            print(f"  {PROCESOS[i]} ESPERA — sin recursos {av}")
            continue

        # simular
        for j in range(3):
            alloc[i][j] += req[j]
            need[i][j] -= req[j]

        if es_seguro():
            rest[i] = DUR[i]
            print(f"  {PROCESOS[i]} ENTRA — alloc={alloc[i]} ({DUR[i]} ciclos)")
        else:
            # rollback
            for j in range(3):
                alloc[i][j] -= req[j]
                need[i][j] += req[j]
            print(f"  {PROCESOS[i]} ESPERA — estado inseguro")

    # cambio
    fase = 1 - fase


print(f"\nCompletado en {minuto} minutos.")
