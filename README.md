# Synth - Generator muzyki

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
przy użyciu biblioteki `pyo`.

## Informacje o zastosowanych metodach i algorytmach

### CustomSynthVisitor
Klasa, w której zdefiniowaliśmy jak generator ma interpretować drzewo składniowe wygenerowane przez SynthParser. Dla każdego rodzaju
wierzchołka zdefiniowaliśmy jakie akcje ma podjąć. W celu rozdzielenia odpowiedzialności za różne funkcje generatora zaimplementowaliśmy
także inne klasy pomocnicze.

### VariableContainer
Klasa odpowiedzialna za tworzenie, przechowywanie i odczytywanie zmiennych. Kontroluje ona również typy zmiennych oraz dba
o to by nazwy zmiennych nie powtarzały się w żadnym zakresie.

### FunctionContainer
Klasa odpowiedzialna za definiowanie i wywoływanie funkcji. Kontroluje ona również typy zwracanych wartości.

### SoundObject
Klasa reprezentująca zmienne przechowujące dźwięk. To w niej zdefiniowane są operacje na dźwiękach.

### MusicHandler
Klasa, której zadaniem jest połączenie zmiennych dźwiękowych w finalny utwór. To tutaj jest deklarowana liczba dostępnych kanałów,
finalna długość utworu oraz nazwa pliku wyjściowego.

## Instrukcja obsługi

W celu wytworzenia pliku dźwiękowego najpierw musimy zapisać opis oczekiwanego dźwięku do pliku tekstowego stosując się
do zasad gramatyki SYNTH. Następnie należy uruchomić skrypt [synth.py](https://github.com/krajewskiML/Teoria-Kompilatorow-i-Kompilacji/blob/master/Synth/synth.py)
wraz z dwoma potrzebnymi argumentami `--generate` (`-g`) w którym podajemy ścieżkę do pliku z opisem dźwięków oraz argumentem `--destination` (`-d`) 
w którym podajemy ścieżkę na którą plik ma zostać zapisany.

Na przykład: `python synth.py -g tests/test3.synth -d outputs/test3.wav`

## Testy i przykłady

1. test1.synth
```
final NCHANNEL = 10, DUR = 25{
    sound a;
    for(idx in range(5)){
        if(idx % 2 == 1){
            a = "turi.wav"@5;
        }else{
            a = "bajpas.wav"@5;
        }
        #1 append a;
    }
}
```

2. test2.synth
```
final NCHANNEL = 4, DUR = 25{
    synth a = Sine(freq=180, add=20, mul=0.2)@10;
    synth d = RCOsc(freq=100, add=1, mul=0.01)@10;
    #3 append [d, a];
}
```

3. test3.synth
```
seq turix(int ile, float trwanie){
    sound a = "turi.wav"@trwanie;
    seq to_return = a * ile;
    return to_return;
}

final NCHANNEL = 4, DUR = 25{
    seq turi = turix(5, 2.85);
    #3 append turi;
}
```

## Możliwe rozszerzenia programu

* Rozszerzenie listy dostępnych generatorów dźwięków
* Udostępnienie dodatkowych parametrów modulacji generowanego dźwięku
* Umożliwienie modulacji wgrywanych utworów

## Ograniczenia programu

* Brak możliwości stworzenia funkcji rekurencyjnych
* Brak dostępu do wartości uderzeń na minutę, zatem brak możliwości zmiany tempa utworu
* Wymóg podania czasu trwania każdego wgranego dźwięku
* Brak możliwości odsłuchu utworu przed jego wygenerowaniem