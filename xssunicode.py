import itertools
import urllib.parse

diccionario_menor = {
    # --- Originales ---
    "⟪": "U+27EA", "≪": "U+226A", "≼": "U+227C", "≺": "U+227A", "《": "U+300A",
    "⟨": "U+27E8", "❮": "U+276E", "〈": "U+3008", "ᐸ": "U+1438", "˂": "U+02C2",
    "﹤": "U+FE64", "＜": "U+FF1C", "˱": "U+02F1", "‹": "U+2039", "<": "U+003C",
    "〈": "U+2329", "≮": "U+226E",
    # --- Nuevos (lista proporcionada) ---
    "«": "U+00AB",   # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    "⋖": "U+22D6",   # LESS-THAN WITH DOT
    "⪅": "U+2A85",   # LESS-THAN OR APPROXIMATE
    "⪡": "U+2AA1",   # DOUBLE NESTED LESS-THAN
}

diccionario_mayor = {
    # --- Originales ---
    "⟫": "U+27EB", "≫": "U+226B", "≽": "U+227D", "≻": "U+227B", "》": "U+300B",
    "⟩": "U+27E9", "❯": "U+276F", "〉": "U+3009", "ᐳ": "U+1433", "˃": "U+02C3",
    "﹥": "U+FE65", "＞": "U+FF1E", "˲": "U+02F2", "›": "U+203A", ">": "U+003E",
    "〉": "U+232A", "≯": "U+226F",
    # --- Nuevos (lista proporcionada) ---
    "»": "U+00BB",   # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "⋗": "U+22D7",   # GREATER-THAN WITH DOT
    "⪆": "U+2A86",   # GREATER-THAN OR APPROXIMATE
    "⪢": "U+2AA2",   # DOUBLE NESTED GREATER-THAN
}

diccionario_comillas_simples = {
    "\u2018": "'", "\u2019": "'", "\u201A": "'", "\u201B": "'", "\u2032": "'",
    "\u2035": "'", "\u00B4": "'", "\u0060": "'", "\u02CB": "'", "\u02CA": "'",
    "\u02B9": "'", "\u02BC": "'", "\u02BD": "'", "\u02F4": "'", "\u055D": "'",
    "\u066C": "'", "\u1FBD": "'", "\u1FBF": "'", "\uFF07": "'", "\uFF40": "'",
    "\u1FEF": "'", "\u02EE": "'"
}

diccionario_comillas_dobles = {
    "\u201C": '"', "\u201D": '"', "\u201E": '"', "\u201F": '"', "\u2033": '"',
    "\u2036": '"', "\uFF02": '"', "\u02DD": '"', "\u02F6": '"', "\u301D": '"',
    "\u301E": '"', "\u301F": '"'
}


def reemplazar_con_correlativo(texto, menor, mayor, contador):
    """
    Reemplaza cada < y > individual por su variante.
    Cada reemplazo incrementa el contador y añade el número
    justo después del texto 'proof' que haya en el payload.
    Devuelve (nuevo_texto, contador_actualizado).
    """
    nuevo = texto

    # Recorremos el texto carácter a carácter para reemplazar < y > individualmente
    # y llevar el correlativo por cada reemplazo.
    resultado = []
    for ch in nuevo:
        if ch == "<" and menor is not None:
            contador += 1
            resultado.append(menor)
            # insertamos el número en el "proof" que venga después
            resultado.append(f"__CORR_{contador}__")
        elif ch == ">" and mayor is not None:
            contador += 1
            resultado.append(mayor)
        else:
            resultado.append(ch)

    nuevo = "".join(resultado)

    # Ahora movemos los marcadores __CORR_N__ al lado del 'proof'
    # Estrategia: reemplazar 'proof' por 'proof' + los números acumulados
    # que aún no se han consumido.
    marcadores = []
    i = 0
    while True:
        idx = nuevo.find("__CORR_", i)
        if idx == -1:
            break
        end = nuevo.find("__", idx + 7)
        if end == -1:
            break
        num = nuevo[idx + 7:end]
        marcadores.append(num)
        nuevo = nuevo[:idx] + nuevo[end + 2:]
        i = idx

    # Insertar los números después de cada 'proof' encontrado
    if marcadores:
        partes = nuevo.split("proof")
        reconstruido = partes[0]
        for j, parte in enumerate(partes[1:]):
            if j < len(marcadores):
                reconstruido += "proof" + marcadores[j] + parte
            else:
                reconstruido += "proof" + parte
        nuevo = reconstruido

    return nuevo, contador


def generar_combinaciones(texto):
    resultados = []

    # Pares sincronizados < >
    pares_tags = list(zip(
        diccionario_menor.keys(),
        diccionario_mayor.keys()
    ))

    # Si no hay < o > usamos un par neutro
    if "<" not in texto and ">" not in texto:
        pares_tags = [(None, None)]

    simples = list(diccionario_comillas_simples.keys()) if "'" in texto else [None]
    dobles = list(diccionario_comillas_dobles.keys()) if '"' in texto else [None]

    for menor, mayor in pares_tags:
        for simple, doble in itertools.product(simples, dobles):

            nuevo = texto

            if simple is not None:
                nuevo = nuevo.replace("'", simple)

            if doble is not None:
                nuevo = nuevo.replace('"', doble)

            # Aplicamos reemplazo de < y > con correlativo
            # El contador se reinicia en 1 para cada combinación
            nuevo, _ = reemplazar_con_correlativo(nuevo, menor, mayor, 0)

            resultados.append(nuevo)

    return resultados


def url_encode_combinaciones(combinaciones):
    return [urllib.parse.quote(c) for c in combinaciones]


def main():
    texto_original = "<s>proof</s>"

    combinaciones = generar_combinaciones(texto_original)

    print(f"\nPayload base: {texto_original}")
    print(f"Total combinaciones generadas: {len(combinaciones)}")

    print("\n=== COMBINACIONES ===\n")
    for c in combinaciones:
        print(c)

    print("\n=== URL ENCODED ===\n")
    for c in url_encode_combinaciones(combinaciones):
        print(c)


if __name__ == "__main__":
    main()
