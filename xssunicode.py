import urllib.parse

diccionario1 = {
    "⟪": "U+27EA", "≪": "U+226A", "≼": "U+227C", "≺": "U+227A", "《": "U+300A",
    "⟨": "U+27E8", "❮": "U+276E", "〈": "U+3008", "ᐸ": "U+1438", "˂": "U+02C2",
    "﹤": "U+FE64", "＜": "U+FF1C", "˱": "U+02F1", "‹": "U+2039", "<": "U+003C",
    "〈": "U+2329", "≮": "U+226E"
}

diccionario2 = {
    "⟫": "U+27EB", "≫": "U+226B", "≽": "U+227D", "≻": "U+227B", "》": "U+300B",
    "⟩": "U+27E9", "❯": "U+276F", "〉": "U+3009", "ᐳ": "U+1433", "˃": "U+02C3",
    "﹥": "U+FE65", "＞": "U+FF1E", "˲": "U+02F2", "›": "U+203A", ">": "U+003E",
    "〉": "U+232A", "≯": "U+226F"
}

# Función para reemplazar y generar combinaciones
def reemplazar_combinacion(texto):
    # Obtener las claves (valores) de ambos diccionarios
    keys1 = list(diccionario1.keys())
    keys2 = list(diccionario2.keys())
    combinaciones = [
        texto.replace("<", key1).replace(">", key2)
        for key1, key2 in zip(keys1, keys2)
    ]
    
    return combinaciones

# Función para codificar en URL
def url_encode_combinaciones(combinaciones):
    return [urllib.parse.quote(combinacion) for combinacion in combinaciones]

# Función principal que maneja la entrada y salida
def main():
    texto_original = input("Introduce el texto que contiene < y > para reemplazar: ")
    # Generar combinaciones de reemplazo
    combinaciones_generadas = reemplazar_combinacion(texto_original)
    # Mostrar combinaciones originales
    print("\nCombinaciones Generadas:")
    for combinacion in combinaciones_generadas:
        print(combinacion)
    # Codificar las combinaciones en URL
    encoded_combinations = url_encode_combinaciones(combinaciones_generadas)
    # Mostrar combinaciones codificadas en URL
    print("\nCombinaciones Codificadas en URL:")
    for encoded in encoded_combinations:
        print(encoded)

if __name__ == "__main__":
    main()
