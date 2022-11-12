#Image base
FROM python:3.8

#Establecemos directorio de trabajo
COPY ./ /app
WORKDIR /app

#Instalacion de dependencias
RUN pip install -r requirements.txt

#Habilitamos el puerto para que sea accesible desde fuera del contenedor
EXPOSE 8181

#Lanzamos la aplicación web
CMD ["python", "./app.py"]

# docker build -t tuguelius/app:2 .

# docker run -p 5000:8181 tuguelius/app:2

# docker login -u tuguelius
# docker push tuguelius/app:2