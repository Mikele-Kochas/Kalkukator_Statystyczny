import streamlit as st

# Funkcja sprawdzająca czy lista zawiera wartości niedodatnie
def sprawdz_czy_niedodatnie(lista_liczb):
    for liczba in lista_liczb:
        if liczba <= 0:
            return True
    return False

# Funkcja obliczająca statystyki
def oblicz_statystyki(lista_liczb):
    lista_liczb = sorted(lista_liczb)
    suma = sum(lista_liczb)
    ilość = len(lista_liczb)
    iloczyn_liczb = 1

    # Obliczenie mediany
    if ilość == 1:
        mediana = lista_liczb[0]
    elif ilość % 2 == 1:
        mediana = lista_liczb[ilość // 2]
    else:
        mediana = (lista_liczb[ilość // 2 - 1] + lista_liczb[ilość // 2]) / 2

    # Dzielenie listy na pół, aby móc obliczyć Q1 i Q3
    if ilość == 1:
        Q1 = lista_liczb[0]
        Q3 = lista_liczb[0]
    else:
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
        if liczba > 0:
            iloczyn_liczb *= liczba
        elif liczba == 0:
            iloczyn_liczb = 0
            break

    # Znalezienie odwrotności liczb, potrzebnej do wyliczenia średniej harmonicznej
    odwrotności_liczb = [1 / liczba for liczba in lista_liczb if liczba != 0]
    suma_odwrotności = sum(odwrotności_liczb)

    # Obliczenie średniej arytmetycznej
    średnia_arytmetyczna = suma / ilość

    # Utworzenie słownika, pełniącego rolę szeregu rozdzielczego
    szereg_rozdzielczy = {}
    for liczba in lista_liczb:
        if liczba not in szereg_rozdzielczy:
            szereg_rozdzielczy[liczba] = 0
        szereg_rozdzielczy[liczba] += 1

    # Obliczenie dominanty
    max_wystąpień = max(szereg_rozdzielczy.values())
    dominanta = [klucz for klucz, wartość in szereg_rozdzielczy.items() if wartość == max_wystąpień]

    # Obsługa błędów dla średniej harmonicznej i geometrycznej
    średnia_harmoniczna = "Niezdefiniowane. Wśród podanych liczb znajdują się liczby niedodatnie"
    if not sprawdz_czy_niedodatnie(lista_liczb) and suma_odwrotności != 0:
        średnia_harmoniczna = ilość / suma_odwrotności

    średnia_geometryczna = "Niezdefiniowane. Wśród podanych liczb znajdują się liczby niedodatnie"
    if not sprawdz_czy_niedodatnie(lista_liczb) and iloczyn_liczb > 0:
        średnia_geometryczna = iloczyn_liczb ** (1 / ilość)

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
    try:
        lista_liczb = [float(liczba.strip()) for liczba in input_text.split(",")]

        if lista_liczb:
            statystyki = oblicz_statystyki(lista_liczb)

            st.write("Szereg rozdzielczy:")
            st.write(statystyki["szereg_rozdzielczy"])

            st.write('Średnia arytmetyczna:')
            st.write(statystyki["średnia_arytmetyczna"])

            st.write("Średnia harmoniczna:")
            if isinstance(statystyki["średnia_harmoniczna"], str):
                st.write(statystyki["średnia_harmoniczna"])
            else:
                st.write(statystyki["średnia_harmoniczna"])

            st.write("Średnia geometryczna:")
            if isinstance(statystyki["średnia_geometryczna"], str):
                st.write(statystyki["średnia_geometryczna"])
            else:
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
    except ValueError:
        st.write("Niepoprawnie wprowadzono dane. Proszę wprowadzić liczby rozdzielone przecinkami.")
