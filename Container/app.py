import joblib
import pandas as pd

pipeline = joblib.load("pipeline.pkl")
model = joblib.load("model.pkl")

def retry_input(function, message=" > El valor introducido es incorrecto."):
    print(message)
    return function()

def get_class():
    data = input("Por favor, introduzca la clase del pasajero. (1),(2) o (3): [1] ")
    if (data.strip() not in ["1", "2", "3", ""]):
        return retry_input(get_class)
    else:
        return data if data != "" else "1"

def get_sex():
    data = input("Introduzca el sexo del pasajero. (M)asculino o (F)emenino: [M] ")
    if (data.upper().strip() not in ["M", "F", ""]):
        return retry_input(get_sex)
    else:
        return data if data != "" else "M"

def get_fare():
    data = input("Introduzca el precio del pasaje: [1000] ")
    try:
        return 1000 if data.strip()=="" else float(data)
    except (ValueError, TypeError):
        return retry_input(get_fare)

def get_age():
    data = input("Introduzca edad (0-999): [25] ")
    try:
        age = 25 if data=="" else int(data)
        return  retry_input(get_age) if age > 999 or age < 0 else age
    except (ValueError, TypeError):
        return retry_input(get_age)


def main():
    print()
    print("****                                           ****")
    print("**** PREDICCIÓN DE SUPERVIVENCIA EN EL TITANIC ****")
    print("****                                           ****")
    print()
    print()

    pclass = get_class()
    sex = get_sex()
    fare = get_fare()
    age = get_age()

    data_array = [pclass, age, fare, "female" if sex == "F" else "male", None]
    column_names = ["pclass", "age", "fare", "sex", "survived"]

    print()
    print("Datos recibidos:")
    df = pd.DataFrame([data_array], columns=column_names)
    print(df)

    print()
    print("Datos transformados:")
    df = pipeline.transform(df).drop("survived", axis=1)
    print(df)

    print()
    print(f"La predicción es que {'SI' if model.predict(df)[0] else 'NO'} sobrevivió")

    print()
    print()
    new_prediction = input("Escribe 'S' para hacer otra predicción : ")
    if new_prediction.strip().upper()=="S":
        main()

main()