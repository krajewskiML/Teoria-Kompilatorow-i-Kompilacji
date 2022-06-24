# Kompilator dla języka generującego muzykę

## Autorzy

1. Konrad Pawlik
2. Maciej Krajewski

## Dane kontaktowe

1. konradpawlik@student.agh.edu.pl
2. krajek@student.agh.edu.pl

## Założenia programu

1. Cele programu:\
  a. Stworzenie pliku WAV na podstawie ciągu instrukcji podanych w pliku wejściowym
2. Rodzaj translatora:\
  a. Generator plików w formacie WAV
3. Język implementacji:\
  a. Python
4. Wykorzystany generator parserów:\
  a. [ANTLR v4](https://www.antlr.org)

## Opis tokenów oraz gramatyka formatu
  [Gramatyka oraz opis tokenów](https://github.com/krajewskiML/Teoria-Kompilatorow-i-Kompilacji/blob/master/Grammar/synth.g4)

## Opis i schemat struktury programu

Nasz projekt składa się z poszczególnych komponentów, <b>synthLexer</b>, czyli skaner kodu, <b>synthParser</b>, jako parser oraz 
<b>synthVisitor</b> czyli wygenerowana klasa, a następnie przystosowana do naszych potrzeb jako generator dźwięków. Program zawiera również
plik <b>Synth.py</b> wykorzystywany w celu uruchomienia programu, a następnie wygenerowania pliku .WAV. 

## Stosowane narzędzia oraz technologie

W celu wygenerowania skanera, parsera oraz generatora dźwięków, a następnie ich obsługiwania wykorzystaliśmy bibliotekę
`antlr4-python3-runtime`. Generowanie dźwięków, ich modulacja oraz wczytywanie własnych plików muzycznych zrealizowaliśmy
przy użyciu biblioteki 'pyo'.

## Informacje o zastosowanych metodach i algorytmach

W celu uzyskania oczekiwanych rezultatów nadpisaliśmy wygenerowane metody klasy synthVisitor. Przy wykorzystaniu atrybutu children
weryfikujemy typ naszego wierzchołka drzewa, a następnie 

## Instrukcja obsługi

## Testy i przykłady

## Możliwe rozszerzenia programu

* Rozszerzenie listy dostępnych generatorów dźwięków
* Udostępnienie dodatkowych parametrów modulacji generowanego dźwięku
* Umożliwienie modulacji wgrywanych utworów

## Ograniczenia programu

* Brak możliwości stworzenia funkcji rekurencyjnych
* Brak dostępu do wartości uderzeń na minutę, zatem brak możliwości zmiany tempa utworu
* Wymóg podania czasu trwania każdego wgranego dźwięku
* Brak możliwości odsłuchu utworu przed jego wygenerowaniem