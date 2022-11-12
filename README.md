# Analítica Escalable

**Miguel Ángel Gárate Lorente (Noviembre 2022)**

Este proyecto contiene los archivos fuentes y artefactos necesarios para dar solución a los cuatro primeros ejercicios de la segunda prueba de evaluación de la asignatura **Analítica Escalable** del Máster en Data Science de la Universidad de Alcalá 2021-2022.

Dentro del directorio Algoritmo, damos solución al primer ejercicio.

Por su parte, el directorio **Container** contiene los artefactos para resolver los ejercicios segundo y tercero.

En último lugar, el directorio **ContainerFlaskML** contiene los artefactos para resolver el cuarto ejercicio.

## 1. Algoritmo
En este directorio encontramos el cuaderno de Jupyter **PEC2.ipynb** con el que hemos entrenado un modelo para predecir la supervivencia de pasajeros del titanic.

El modelo ha sido entrenado con el archivo **titanic.csv** contenido en el mismo directorio.

La ejecución completa del cuaderno supone la exportación, a través de joblib, de dos objetos que pueden ser reutilizados en entornos de producción:

* **Pipeline de tratamiento de datos** (exportado como pipeline.pkl)
* **Modelo de regresión logística entrenado** (model.pkl)

### 1.1 Pipeline de tratamiento de datos
Emplearemos este pipeline para transformar los datos como paso previo a su uso como entrada en el modelo de predcción. El pipeline consta del siguiente conjunto secuencial de operaciones:

* Generación mediante **OneHotEncoder** de variables dummies para la variable categórica *sex*

* Eliminación de las características: *name, sibsp, parch, ticket, cabin, embarked*

* Eliminación de registros con algún valor nulo

* Normalización de valores mediante **StandardScaler** de sklearn 

### 1.2 Modelo de predicción
Para llevar a cabo la predicción, se ha empleado un modelo de regresión logística embebido en un modelo GridSearchCV que permite establecer el conjunto de hiperparámetros óptimo para los datos de entrenamiento contenidos en el archivo **titanic.csv**

## 2. Contenedor del Algoritmo
El directorio **Container** contiene todo lo necesario para generar un contenedor de Docker que lanza el programa **app.py** que emplea los dos objetos pkl generados a partir del cuaderno de Jupyter para realizar predicciones:

* Pipeline de tratamiento de datos: **pipeline.pkl**
* Modelo de predicción entrenado: **model.pkl**

### 2.1 Programa app.py
El programa realiza predicciones en base a ciertas características introducidas por el usuario mediante consola. Esto hace que dicho programa no haga predicciones de manera automática (o desatendida) sino que dependa de la intervención del usuario. 

En un entorno productivo lo lógico es contar con un programa que realice predicciones de manera automática y, por tanto, sin intervención del usuario. Sin embargo, el propósito del programa es mostrar el uso de un modelo previamente entrenado embebido en un contenedor de Docker.

### 2.2 Generación de la imagen de Docker 
Nos ubicamos en el directorio **Container**: 
```
cd Container
```

Y empleamos el siguiente comando para generar la imagen:
```
cd Container
docker build -t tuguelius/app:1 .
```

### 2.3 Publicación en Docker Hub
Para la publicación de la imagen de la **versión 1** de la aplicación, empleamos los siguientes comandos:

```
docker login -u tuguelius
docker push tuguelius/app:1
```

### 2.4 Descarga de la imagen publicada en Docker Hub
Ejecutaremos el siguiente comando:

```
docker pull tuguelius/app:1 
```

### 2.5 Ejecución del contenedor de Docker
Al ser un programa interactivo, el comando que necesitaremos emplear deberá incluir las opciones **-ti**. Así, el comando será el siguiente:

```
docker run -ti tuguelius/app:1
```

## 3. Contenedor del Algoritmo como API
Mediante el uso de la librería Flask de Python, construimos la segunda versión de la aplicación de predicción de supervivencia del Titanic.

La aplicación levanta un servicio web en el puerto 8181 que sirve un formulario HTML en la ruta raiz para poder realizar predicciones, esto es, http://localhost:8181/

El servicio responde a peticiones POST y GET. 

Basta con emplear el formulario web para enviar peticiones de tipo POST. Es necesario especificar todos los valores y que éstos sean correctos para obtener una predicción correcta. En otro caso, el servicio retornará un error interno. 
La invocación mediante POST mostrará el resultado embebido en el mismo formulario HTML empleado para hacer la petición. 

Para invocarlo mediante GET, basta con incluir los parámetros en la URL. Por ejemplo:

http://localhost:8181/?pclass=2&sex=female&age=66&fare=100

La invocación mediante GET mostrará el resultado en formato JSON. 

### 3.1 Generación de la imagen de Docker 
Nos ubicarmos dentro del directorio **ContainerFlaskML**:
```
cd ContainerFlaskML
```

Empleamos el siguiente comando para generar la imagen:
```
docker build -t tuguelius/app:2 .
```

### 3.2 Publicación en Docker Hub
Para la publicación de la imagen de la **versión 2** de la aplicación, empleamos los siguientes comandos:

```
docker login -u tuguelius
docker push tuguelius/app:2
```

### 3.3 Descarga de la imagen publicada en Docker Hub
Ejecutar el siguiente comando:
```
docker pull tuguelius/app:2 
```


### 3.4 Ejecución del contenedor de Docker
Para ejecutar la aplicación debemos considerar el mapping de un puerto local para que haga de puente sobre el puerto 8181 del servicio web del contenedor Docker. 

Suponiendo que queremos emplear nuestro puerto local 5000, debemos emplear el siguiente comando:

```
docker run -p 5000:8181 tuguelius/app:2
```

Una vez levantado el contenedor, basta con abrir la siguiente URL en nuestro navegador:

http://localhost:5000/

Ejemplo de invocación mediante GET:

http://localhost:5000/?pclass=2&sex=female&age=66&fare=100




