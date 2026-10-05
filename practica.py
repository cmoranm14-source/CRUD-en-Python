ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil"]
vistas = set()
unicas = []
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)
print(unicas)

conteo = {}
for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1     # .get evita el KeyError la primera vez
print(conteo)
# El más repetido:
mas_repetida = max(conteo, key=conteo.get)
print(mas_repetida)


inscritos_matematica = {"Ana","Luis","Sol","Marco"}
inscritos_ingles = {"Luis","Marco","Ruth"}
ambas = inscritos_matematica & inscritos_ingles 
solo_mate = inscritos_matematica - inscritos_ingles 
total = len(inscritos_matematica | inscritos_ingles)
print(sorted(ambas), sorted(solo_mate), total)


clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}]
indice = {cliente["id"]: cliente for cliente in clientes}
print(indice[2]["nombre"])


ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
total = sum(monto for _mes, monto in ventas)
mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])
print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")
for mes, monto in ventas:              # desempaquetado en el for
    print(f"{mes:<10} {monto}")


