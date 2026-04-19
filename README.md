# Algoritmo del Banquero 

## Definición

El **Algoritmo del Banquero**, propuesto por Edsger Dijkstra, es un método de control de recursos utilizado para **evitar interbloqueos (deadlocks)** en sistemas concurrentes.

Su idea principal es simple:

> Un sistema solo concede recursos si al hacerlo **permanece en un estado seguro**.

Un **estado seguro** es aquel en el que existe al menos un orden en el que todos los procesos pueden terminar sin quedarse bloqueados.

---

## Cómo funciona

El algoritmo trabaja con cuatro estructuras fundamentales:

- **TOTAL** → recursos disponibles en el sistema  
- **MAX** → demanda máxima de cada proceso  
- **alloc** → recursos actualmente asignados  
- **need** → recursos que aún necesita cada proceso  

Se cumple:
`need = MAX - alloc`


Cuando un proceso solicita recursos:

1. Se verifica si hay recursos suficientes (`available`)
2. Se asignan temporalmente (`simulación`)
3. Se evalúa si el sistema sigue siendo seguro
4. Si es seguro → se concede la solicitud  
5. Si no → se revierte la asignación (`rollback`)

---

## Estado seguro

Un estado es seguro si existe un orden en el que todos los procesos pueden terminar liberando sus recursos.

El algoritmo simula ese orden para comprobar si es posible.

Si no existe, el sistema entra en un **estado inseguro**, y la solicitud se rechaza.

---

## Implementación en el código

En la simulación del cruce vehicular:

### Recursos

```python
TOTAL = [20, 50, 30]
```

Representan la capacidad del sistema:

20 → espacio en el centro del cruce
50 → capacidad horizontal
30 → capacidad vertical

### Procesos

Cada dirección del tráfico es un proceso:

P1, P2 → horizontal
P3, P4 → vertical

### Estado del sistema
```python
alloc = [[0]*3 for _ in range(4)]
need  = [row[:] for row in MAX]
```
alloc → recursos que cada proceso está usando

need → recursos que le faltan para terminar

### Recursos disponibles
```python
def available():
    return [TOTAL[j] - sum(alloc[i][j] for i in range(4)) for j in range(3)]
```

Calcula los recursos libres en el sistema en cada momento.

### Verificación de estado seguro
```python
def es_seguro():
```
Esta función simula la ejecución de los procesos:

- Busca un proceso que pueda terminar con los recursos disponibles
- Simula que termina y libera recursos
- Repite el proceso

Si todos pueden terminar → estado seguro
Si alguno queda bloqueado → estado inseguro

### Asignación de recursos

Cuando un proceso intenta entrar:

- Se calcula su solicitud (need)
- Se verifica contra available
- Se asigna temporalmente
- Se ejecuta es_seguro()
```python  
#asignación temporal
alloc[i][j] += req[j]
need[i][j] -= req[j]
```
Si es seguro → el proceso entra
Si no → se deshace:
```python  
alloc[i][j] -= req[j]
need[i][j] += req[j]
```

## Idea clave

Aunque haya recursos disponibles, el sistema puede rechazar una solicitud si compromete la seguridad futura.

Esto es lo que diferencia al algoritmo del banquero de una asignación simple:

No decide solo por el presente, sino por la viabilidad del sistema completo.

# Conclusión

En este código, el algoritmo del banquero se aplica para:

- controlar el acceso de vehículos al cruce
- evitar saturación del sistema
- garantizar que todos los procesos puedan terminar

No busca maximizar el flujo, sino mantener el sistema seguro y libre de bloqueos.
