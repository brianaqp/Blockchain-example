Que falta actualmente?
* Resuelto
- Se debe reflejar el dinero transferido en las cuentas. 
- Se almacen las transacciones por cuenta. No se almacenan las que se rechazan antes de
  instanciarse. 
- En la clase Blockchain se añadio una condional que cambia el estado de las transacciones, regresando el dinero al que realizo la transaccion.

* Pendiente
- Prestar atencion al proceso. (tx -> sign -> verify -> blockchain). Puede estar mal.


- Definir si sera proof of work o proof of stake. (Mas que definir, poner los dos ejemplos.)

- PLAN ACTUAL
añadir proof of stake:
1.- Que se incluyan validadores
2.- Se escojan al azar
3.- Validan la transaccion
4.- Añada un bloque

Investigacion: La forma de validar el bloque seria como revisar la firma de una transaccion.

hash = last_block.hash
_hash = hash(last_block.__dict__)
if hash = _hash:
    validated.