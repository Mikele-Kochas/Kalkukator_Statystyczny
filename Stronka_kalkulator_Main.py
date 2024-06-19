import streamlit as st

# Funkcja obliczająca statystyki
def oblicz_statystyki(lista_liczb):
    lista_liczb = sorted(lista_liczb)
    suma = sum(lista_liczb)
    ilość = len(lista_liczb)
    iloczyn_liczb = 1

    # Obliczenie mediany
    if ilość % 2 == 1:
        mediana = lista_liczb[ilość // 2]
    else:
        mediana = (lista_liczb[ilość // 2 - 1] + lista_liczb[ilość // 2]) / 2

    # Dzielenie listy na pół, aby móc obliczyć Q1 i Q3
    if ilość % 2 == 0:
        pierwsza_połowa = lista_liczb[:ilość // 2]
        druga_połowa = lista_liczb[ilość // 2:]
    else:
        pierwsza_połowa = lista_liczb[:ilość // 2]
        druga_połowa = lista_liczb[ilość // 2 + 1:]

    # Obliczanie Q1
    if len(pierwsza_połowa) % 2 == 1:
        Q1 = pierwsza_połowa[len(pierwsza_połowa) // 2]
    else:
        Q1 = (pierwsza_połowa[len(pierwsza_połowa) // 2 - 1] + pierwsza_połowa[len(pierwsza_połowa) // 2]) / 2

    # Obliczanie Q3
    if len(druga_połowa) % 2 == 1:
        Q3 = druga_połowa[len(druga_połowa) // 2]
    else:
        Q3 = (druga_połowa[len(druga_połowa) // 2 - 1] + druga_połowa[len(druga_połowa) // 2]) / 2

    # Obliczenie iloczynu liczb, potrzebnego do wyliczenia średniej geometrycznej
    for liczba in lista_liczb:
        if liczba != 0:
            iloczyn_liczb *= liczba

    # Znalezienie odwrotności liczb, potrzebnej do wyliczenia średniej harmonicznej
    odwrotności_liczb = [1 / liczba for liczba in lista_liczb if liczba != 0]
    suma_odwrotności = sum(odwrotności_liczb)

    średnia_arytmetyczna = suma / ilość
    średnia_harmoniczna = ilość / suma_odwrotności
    średnia_geometryczna = iloczyn_liczb ** (1 / ilość)

    # Utworzenie słownika, pełniącego rolę szeregu rozdzielczego
    szereg_rozdzielczy = {}
    for liczba in lista_liczb:
        if liczba not in szereg_rozdzielczy:
            szereg_rozdzielczy[liczba] = 0
        szereg_rozdzielczy[liczba] += 1

    # Obliczenie dominanty
    max_wystąpień = max(szereg_rozdzielczy.values())
    dominanta = [klucz for klucz, wartość in szereg_rozdzielczy.items() if wartość == max_wystąpień]

    return {
        "średnia_arytmetyczna": średnia_arytmetyczna,
        "średnia_harmoniczna": średnia_harmoniczna,
        "średnia_geometryczna": średnia_geometryczna,
        "mediana": mediana,
        "dominanta": dominanta,
        "Q1": Q1,
        "Q3": Q3,
        "szereg_rozdzielczy": szereg_rozdzielczy
    }

# Streamlit interfejs użytkownika
st.set_page_config(page_title="Kalkulator Statystyczny")
st.subheader("Nie bierz tej stronki zbyt poważnie, dopiero się uczę")
st.title("Kalkulator Statystyczny")

input_text = st.text_area("Wprowadź liczby rozdzielone przecinkami:", "1, 2, 3, 4, 5")

if st.button("Oblicz statystyki"):
    lista_liczb = [float(liczba) for liczba in input_text.split(",")]

    statystyki = oblicz_statystyki(lista_liczb)

    st.write("Szereg rozdzielczy:")
    st.write(statystyki["szereg_rozdzielczy"])

    st.write('Średnia arytmetyczna:')
    st.write(statystyki["średnia_arytmetyczna"])

    st.write("Średnia harmoniczna:")
    st.write(statystyki["średnia_harmoniczna"])

    st.write("Średnia geometryczna:")
    st.write(statystyki["średnia_geometryczna"])

    st.write("Mediana:")
    st.write(statystyki["mediana"])

    st.write("Dominanta:")
    for value in statystyki["dominanta"]:
        st.write(value)

    st.write("Kwartyle:")
    st.write("Q1: ")
    st.write(statystyki["Q1"])

    st.write("Q2: ")
    st.write(statystyki["mediana"])

    st.write("Q3: ")
    st.write(statystyki["Q3"])
