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