#Image base
FROM python:3.8

#Establecemos directorio de trabajo
COPY ./ /app
WORKDIR /app

#Instalacion de dependencias
RUN pip install -r requirements.txt

#Habilitamos el puerto para que sea accesible desde fuera del contenedor
CMD ["python", "./app.py"]

# PARA CREAR EL CONTENEDOR
# docker build -t tuguelius/app:1 .

# PARA EJECUTAR
# docker run -ti tuguelius/app:1 .

# PARA SUBIR CONTENEDOR
# docker login -u tuguelius
# docker push tuguelius/app:1