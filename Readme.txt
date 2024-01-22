Desarrollo: JR Jeisson Ramirez Bravo

prueba tecnica desarrollador backend 

API REST - FastApi 

El desarrollo se realiza con apoyo de  las aplicacones web, fatsAPI, uvicorn y visual code.
que nos permite sean ejecutadas en el lenguaje de programacion python.

Fast API el  marco o entortno web a utilizar 
Uvicorn el  SERVIDOR para utilizar aplicaciones asincronas en python mediante solicitudes HTTP.

en visual code se crea al archivo con extension .py (Python) se establecer los aprametros, estructura y funcionalidad para ser ejecutado.

se instala mediate termianl las  instancias de  fastApi, uvicorn y python 3.7.

para la instalacion :
pip install fastapi uvicorn

para la ejecucion:
uvicorn main:app --reload
  una vez ejecudao el comando en al terminal no dirigimos a la  direccion: 
http://127.0.0.1:8000/docs
habilitada por Uvicorn

alli podrmos identificar la funcionalidad de la APi

donde encontramos:

Implementacion de  los metodos, POST, GET en los distintos CRUD solicitados,  

para registrar o consultar algun item ejecutamos  Try it out(Prueba)
ingresamos los parametros y damos en ejecutar.
obtendremos  2  tipos de respuesta, negativa  y positva. 
si los datos son ingresados o consultados son de manera correcta  nos dara respuesta de 200 
si los datos consultados son erroneos btendremos  una respuesta de  400 

la FastApi se crea usando dicccionarios para cada CRUD con sus Primary Key y sus ForeingKey 
 impementando los metodos GET, POST, realizando prubas apoyado de la herramienta postman.

para establecer la recepcion y envio de token jutno a cada registro y consulta de datos.



qudo atento a cualqueir novedad,
muchas gracias de antemano.

att: 
JR Jeisson Ramirez Bravo 
3115802661



