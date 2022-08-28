# Que falta actualmente?
**Resuelto
- Se debe reflejar el dinero transferido en las cuentas. 
- Se almacen las transacciones por cuenta. No se almacenan las que se rechazan antes de
  instanciarse. 
- En la clase Blockchain se añadio una condional que cambia el estado de las transacciones, regresando el dinero al que realizo la transaccion.

**Pendiente
- Prestar atencion al proceso. (tx -> sign -> verify -> blockchain). Puede estar mal.
- Definir si sera proof of work o proof of stake. (Mas que definir, poner los dos ejemplos.)
- Incluir el Merkle Root

# PLAN ACTUAL
**Leer el link de abajo
> Investigacion: La forma de validar el bloque seria como revisar la firma de una transaccion.
Pagina muy buena que me contiene informacion de PoS
https://medium.com/techskill-brew/proof-of-stake-or-pos-in-blockchain-part-8-blockchain-basics-32d461232e1c#:~:text=Forging%20and%20forger%3A%20In%20the,known%20as%20validators%20or%20forgers.

Lo que debo de hacer ahora es seguir lo que dice la pagina de arriba para incluir Proof Of Stake

# Lo que sigue:
Sigo en la funcion de add_tx, pero especificamente en:
- Forjador firma el bloque. (Hace la firma)
- Los demas validadores deberian de revisar que esa firma sea correcta. (Aqui voy.)