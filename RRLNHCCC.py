import numpy as np
import re
from sympy.parsing.sympy_parser import parse_expr
import sympy as sp
from fractions import Fraction

def extraer_coeficientes(ecuacion): #Extraido de ChatGPT
    coeficientes = []           # Creamos una lista vacía para almacenar los coeficientes
    partes = ecuacion.split('*f(n')  # Dividimos la ecuación en partes usando el separador "*f(n"
    for parte in partes:        # Para cada parte de la ecuación
        coef = ''              # Inicializamos una cadena vacía para almacenar el coeficiente
        for char in reversed(parte):  # Iteramos por cada caracter de la parte, en orden inverso
            if char.isdigit() or char in ['-', '+', '.']:  # Si el caracter es un dígito, signo o punto decimal
                coef += char   # Lo agregamos a la cadena del coeficiente
            else:
                break         # Si no es un dígito, signo o punto decimal, paramos el ciclo
        coef = coef[::-1]      # Invertimos la cadena del coeficiente
        if coef:
            coeficientes.append(float(coef))  # Si el coeficiente no está vacío, lo convertimos a flotante y lo agregamos a la lista
        else:
            coeficientes.append(1)  # Si el coeficiente está vacío, asumimos que es 1 y lo agregamos a la lista
    ultimo = coeficientes.pop()  # Quitamos el último elemento de la lista
    coeficientes.insert(0, ultimo)  # Insertamos el último elemento en la primera posición de la lista
    for i in range(1, len(coeficientes)):
        coeficientes[i] *= -1   # Multiplicamos cada coeficiente excepto el primero por -1
    return coeficientes          # Devolvemos la lista de coeficientes

def encontrar_k(ecuacion): #Extraido de ChatGPT
    k = 0  # Inicializar k en cero
    idx = ecuacion.find('f(n-')  # Buscar la primera aparición de 'f(n-'
    while idx != -1:  # Mientras haya más apariciones
        idx += 4  # Saltar los caracteres 'f(n-'
        numero = ''  # Inicializar una cadena vacía para el número
        while idx < len(ecuacion) and ecuacion[idx].isdigit():  # Buscar dígitos después de 'f(n-'
            numero += ecuacion[idx]  # Concatenar el dígito a la cadena
            idx += 1  # Avanzar el índice
        if numero:  # Si se encontró un número
            k = max(k, int(numero))  # Actualizar k si es mayor que el valor actual
        idx = ecuacion.find('f(n-', idx)  # Buscar la siguiente aparición de 'f(n-' a partir del índice actual
    return k  # Devolver el valor máximo de k encontrado



def crear_matriz(raices, valores):
  M=np.zeros([len(valores),len(raices)]) # Creamos una matriz de ceros con tamaño de valores y el tamaño de las raices
  for j in range(len(valores)): # Iteramos por las filas, es decir las f(n)
    m=0 # Creamos un contador que nos va a servir para elevar las n
    for i in range(len(raices)): # Iteramos sobre las b
      
      if i==0:
        M[j][i]=raices[i]**j # Si es la primera queda igual y solo se multiplica por la raiz a la n
        m=m+1 # Aumentamos el contador
      else:
        if raices[i]==raices[i-1]: # Si es igual que la anterior entonces se multiplica por un n
          M[j][i]=(raices[i]**j)*(j**m) # Multiplicamos la R^n * n^m, m siendo el contador de multiplicidad
          m=m+1 # Aumentamos el contador
        elif raices[i]!=raices[i-1]: # Si es diferente a la raiz anterior entonces
          m=0 # El contador de multiplicidad lo ponemos en 0
          M[j][i]=(raices[i]**j)*(j**m) # Elevamos la raiz a la n y multiplicamos por n^m
          m=m+1 # Aumentamos el contador
  return M

def crear_norecurrente(b, raices):
  s="" # Creamos una string
  aux=0
  contador=0
  for i in range(len(raices)): # Iteramos sobre las raices para añadirles sus n
      if i==0:
        s = s + str(b[aux]*raices[i]) + "**n + " # Al primero lo elevamos a la n
        aux = aux + 1
      else:
        if raices[i]==raices[i-1] and (i!= len(raices)-1): # Si es igual al anterior y no es la final
          s = s  + str(b[aux]) + "*n**" + str(i) + "*"+ str(raices[i]) + "**n + " # Elevamos n al contador y añadimos la raiz
          aux = aux + 1
        if raices[i]==raices[i-1] and (i== len(raices)-1): # Si es igual y es la final
          s = s  + str(b[aux]) + "*n**" + str(i) + "*"+ str(raices[i]) + "**n" # Lo mismo pero no le añadimos el +
          aux = aux + 1
        if raices[i]!=raices[i-1] and (i!= len(raices)-1): # Si es diferente y no es la final
          s = s + " " + str(b[aux]) + str(raices[i]) + "**n + " # Elevamos la raiz a la n
        if raices[i]!=raices[i-1] and (i== len(raices)-1):
          s = s + " " + str(b[aux]) + str(raices[i]) + "**n" # Lo mismo pero no le añadimos el +
  return s


def find_largest_number(s): 
    # Busca 'n**'
    m = re.findall(r'n\*\*(\d+)', s)
    if m:
        return max([int(n) for n in m])
    
    # Busca 'n' no precedido por '**'
    m = re.findall(r'(?<!\*\*)n(?!\*)', s)
    if m:
        return 1
    
    # No se encontró 'n' ni 'n**'
    return 0

def find_num_before_n(string): # Encuentra el numero a la izquierda de un **n, para saber cual es la r^n
    regex = r'(\d+)\*\*n'
    match = re.search(regex, string)
    if match:
        return int(match.group(1))
    else:
        return 1
    
def casos(recurrence, k, gn, t, rn): # La funcion usa sympy para poder encontrar los valores de A,B,C dependiendo del caso
  if (t==1):
    #Caso g(n) -> An+B
    print('Caso An+B')
    for i in range(1,k+1):
      if f'f(n-{i})' in recurrence:
        recurrence = recurrence.replace(f'f(n-{i})',f'(A*(n-{i})+B)')

    f_fp = sp.simplify(parse_expr(recurrence)) #Lo convierte en expresion matematica.      
    A,B,n = sp.symbols('A B n')
    eq = sp.Eq(A*n + B, f_fp)
    sol = sp.solve(eq, (A, B))
    sol_inlist = [sol[i] for i in sol]
    return sol_inlist

  if (t==2):
    #Caso g(n) -> n^2
    print('Caso An^2 + Bn + C')
    for i in range(1,k+1):
      if f'f(n-{i})' in recurrence:
        recurrence = recurrence.replace(f'f(n-{i})',f'(A*(n-{i})**2+B*(n-{i})+C)')
    f_fp = sp.simplify(parse_expr(recurrence))
    n, A, B, C = sp.symbols('n A B C')
    eq = sp.Eq(A*n**2 + B*n + C, f_fp)
    sol = sp.solve(eq, (A, B, C))
    sol_inlist = [sol[i] for i in sol]
    return sol_inlist

  if (t==0 and rn==1):
    #Caso g(n) -> C
    print('Caso C')
    for i in range(1,k+1):
      if f'f(n-{i})' in recurrence:
          recurrence = recurrence.replace(f'f(n-{i})',f'C')
    f_fp = sp.simplify(parse_expr(recurrence)) #Lo convierte en expresion matematica.
    C = sp.symbols('C')
    eq = sp.Eq(C, f_fp)
    sol = sp.solve(eq, C)
    return sol

  if (t==0 and rn>1):
    #Caso g(n) -> R**n
    print('Caso C*R^n')
    ind = f'{gn}'.index('n')
    new = f'{gn}'[:ind]+'('+ f'{gn}'[ind:] +')'
    print(new)
    
    for i in range(1,k+1):      
      if f'f(n-{i})' in recurrence:
          recurrence = recurrence.replace(f'f(n-{i})','C*'+new.replace('n',f'n-{i}'))
    f_fp = sp.simplify(parse_expr(recurrence))             
    n,C = sp.symbols('n C')
    eq = sp.Eq(C*int(f'{gn}'[1])**n, f_fp)
    sol = sp.solve(eq, C)
    return sol

def cambiar_valores(t, valores, coeficientes_abc, rn): # La funcion resta el valor inicial con el valor de An^2+Bn+C dependiendo del caso
  if (t==1):
    for i in range(len(valores)): # Itera sobre los valores
      valores[i] = valores[i] - ((coeficientes_abc[0]*i) + coeficientes_abc[1]) # f(n) - (An+B)
  if(t==2):
    for i in range(len(valores)):
      valores[i] = valores[i] - (coeficientes_abc[0]*(i**2) + coeficientes_abc[1]*i + coeficientes_abc[2])  # f(n) - (An^2+Bn+c)
  if (t==0 and rn==1):
    for i in range(len(valores)):
      valores[i]= valores[i] - coeficientes_abc[0]  # f(n) - C
  if (t==0 and rn>1):
    for i in range(len(valores)):
      valores[i]= valores[i] - (coeficientes_abc[0]*(rn**i))  # f(n) - (C*R^n)
  return valores

def separar_gn(cadena):
    # Define la expresión regular para buscar términos del tipo a*f(n-b)
    patron = r'([+-]?\s*\d*\s*\*\s*f\s*\(\s*n\s*-\s*\d+\s*\))'

    # Busca todas las coincidencias del patrón en la cadena
    terminos_afn = re.findall(patron, cadena)
    terminos_afn_str = ''.join(terminos_afn) #+ a las comillas
    


    # Elimina los términos del tipo a*f(n-b) de la cadena original
    cadena_sin_afn = re.sub(patron, '', cadena)

    # Retorna los términos del tipo a*f(n-b) y la cadena sin estos términos
    return terminos_afn_str, cadena_sin_afn
    
def crear_norecurrente_nh(b, raices, abc, t, rn): # Hace lo mismo que la recurrente pero esta vez dependiendo del caso le añade las A,B,C
  s = crear_norecurrente(b, raices)
  if (t==1):
    s = s + " + " + str(abc[0]) + "*n + " + str(abc[1]) # Añade el An+B
  if (t==2):
    s = s + " + " + str(abc[0]) + "*n**2 + " + str(abc[1]) + "*n + " + str(abc[2]) # Añade el An^2+Bn+c
  if (t==0 and rn==1):
    s = s + " + " + str(abc[0]) # Añade el C
  if (t==0 and rn>1):
    s = s + " + " + str(abc[0]) + "**n" # Añade el C*R^n
  return s


def solucionar_no_homogenea(funcion,valores_iniciales):
  fn,gn = separar_gn(funcion)
  print('gn: ', gn)
  print('fn: ', fn)
  coeficientes_float2 = extraer_coeficientes(fn)
  coeficientes_int2 = [int(f) for f in coeficientes_float2]
  raices2 = np.around(np.roots(coeficientes_int2))
  k2 = encontrar_k(fn)
  t=find_largest_number(gn)
  valores_iniciales2=[int(numero) for numero in valores_iniciales.split(',')]
  rn = find_num_before_n(gn)
  coeficientes_abc = casos(funcion, k2, gn, t, rn)
  valores_iniciales_2=cambiar_valores(t,valores_iniciales2, coeficientes_abc, rn)
  valores2=np.array(valores_iniciales_2, dtype=np.float64)
  matriz2 = crear_matriz(raices2, valores_iniciales_2)
  coeficientes_resultado = np.linalg.solve(matriz2, valores2)
  no_recurrente = crear_norecurrente_nh(coeficientes_resultado, raices2, coeficientes_abc, t, rn)
  print('no recurrente: ', no_recurrente)
  return no_recurrente
