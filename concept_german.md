Modales Text-Diff zwischen Dateien
==================================

Diff-Tests für Software laufen etwa so ab:
* Software wird gestartet
* ein bestimmtes Makro läuft durch
* das out-Verzeichnis wird gegen ein Referenzverzeichnis gedifft
*  Im Diff werden Zeilen, die zu Ignore-Mustern passen, ignoriert
*  Zeilen, die zu Replacement-Mustern passen, werden ersetzt

Für manche Tests funktioniert dieses simple Vorgehen nicht:
* Numerische Differenzen in Matrizen und Zahlenkolonnen müssen geprüft
  werden, weder kann eine solche Zeile einfach ignoriert oder durch
  etwas anderes ersetzt werden.

Für solche Fälle wurde schon mit Spiff experimentiert.

Grundidee
---------

In die Listenausgabe sollen zusätzliche Hints geschrieben werden,
die es erlauben die Ausgabe "intelligenter" mit dem Referenzstand zu
vergleichen. Wir wollen also einen Ersatz für das simple Diff schreiben

Beispiel numdiff ===

    <tio:numdiff expr="
    (skip 2 lines)
        (n times
            (int>0)(s+)(real 0.69315~0.00001)(s+)(real 0.69315~0.00001)(s+)(real 6.93147E-01~1E-3)(s+)(real 693.14718E-03~1E-3))" skip_emptylines="true">

                 1    1    2    2    3    3    4    4    5    5    6    6    7    7
        ....5....0....5....0....5....0....5....0....5....0....5....0....5....0....5
          1   2.00000    0.69315E+00   0.69315E+000    6.93147E-01  693.14718E-03
          2   1.80000    0.58779E+00   0.58779E+000    5.87787E-01  587.78661E-03
          3   1.60000    0.47000E+00   0.47000E+000    4.70004E-01  470.00358E-03
          4   1.40000    0.33647E+00   0.33647E+000    3.36472E-01  336.47212E-03
          5   1.20000    0.18232E+00   0.18232E+000    1.82321E-01  182.32140E-03
          6   1.00000   -0.17881E-06  -0.17881E-006   -1.78814E-07 -178.81395E-09
          7   0.80000   -0.22314E+00  -0.22314E+000   -2.23144E-01 -223.14376E-03
          8   0.60000   -0.51083E+00  -0.51083E+000   -5.10826E-01 -510.82587E-03
          9   0.40000   -0.91629E+00  -0.91629E+000   -9.16291E-01 -916.29112E-03
         10   0.20000   -0.16094E+01  -0.16094E+001   -1.60944E+00   -1.60944E+00

    </tio:numdiff>

Parst alle Zeilen im <numdiff>-Tag nach dem in expr gegebenen Ausdruck. Dies geschieht sowohl in der Referenz als auch in der neuen Ausgabe.

Beispiel skip ===

    <tio:skip>

        Bla Bla bla
        Foo Diff 5 7 Ertrag
        5.74 -2.5163E-1

    </tio:skip>

Die folgenden Zeilen werden komplett übersprungen. Im Default wird geprüft, ob die Anzahl an Zeilen übereinstimmt.

Beispiel lclsubst ===

    <tio:lclsubst subst="
    'TEXTZ \"([^\"]+)\"' => <descr>         #Textz kann aufgrund blabla abweichen
    '!(.+)'              => !<comment>">    #Kommentare können sich unterscheiden wegen...
    LENS
    TEXTZ "dies ist irgendeine Beschreibung"

    S S0
    S S1
    S S2
    S S3
    S S4
    S S5

    </tio:lclsubst>

Innerhalb von lclsubst gelten die im subst-Attribut definierten Substitutionals.

Beispiel expectmatch ===

    <tio:expectmatch expr="(errormsg 'S7')"

    PRINT "HI"
    PRINT {LDM R S7}


        ERROR -- Ungueltiger Qualifier S7

    </tio:expectmatch>

Beispiel multiline ===

    <tio:multiline>
        ERROR -- Kann Datei /home/zomkoer/test
        /34_fef/fefve01_test.oase nicht oeffne
        n
    </tio:multiline>

In dem multiline-Abschnitt wird der Diff nicht
zeilenweise gebildet sondenr Zeilenumbrüche ignoriert
und die resultierende Gesamtzeile gediff'ed.

Multiline ist kein Tester sondern ein Filter. Hintendran kann
ein Standard-Diff stehen (wenn kein weiteres tio:-Element gegeben ist)
oder auch ein numdiff-Test. Dann muss man es schachteln

Beispiel diff ===

    <tio:diff ignore_whitespace="false">
    Bla
        Eingeruecktes Bla
        Eingeruecktes Bla2
    </tio:diff>

Durch diff kann ein eigener Diff-Abschnitt aufgemacht werden, der
zum einen von den dateiweiten Einstellungen abweichende diff-Optionen
erlaubt und zum anderen die Menge der zu diffenden Zeilen festsetzt.

Implementierung
---------------

Wir haben spezielle "Tester" für die verschiedenen Abschnitte.
In einem Tester wollen wir prinzipiell folgende Syntax haben:

    for line in lines:
        ...

wobei lines ein Generator ist, damit wir die Datei oder einzelne
Abschnitte nicht komplett einlesen müssen.

Neben Testern gibt es auch Filter, welche dazwischengeschaltet werden
und z.Bsp. Zeilen vorverarbeiten bevor sie an den eigentlichen Tester
übergeben werden.

Für das Ende der Zeile hinter <tio:...> sowie für den Anfang der Zeile
vor <tio:...> wird der Rest als Zeile zurückgeliefert von diesem
Generator.

Unterscheiden sich die XML-Elemente von Referenz und Ausgabe, wird
dies als Unterschied gewertet und eine Fehlermeldung geworfen. Dabei
werden XML-unwesentliche Unterschiede ignoriert (z.Bsp. Anzahl Leerzeichen
zwischen zwei Attributen)

Dann hätten wir also folgende Module:
* Zeilenleser
* Tester-Umschalter
* Tester
 * numdiff
 * skip
 * expectmatch
 * diff
* Filter
 * lclsubst
 * multiline
 * lowercase
* Ausgabe
* Kommandozeilen-Schnittstelle

Syntax für Grammatiken
----------------------

WICHTIG: Wir setzen diese eigene Syxntax erst ein mal nicht um.

Patterns sollen durch eine möglichst gut lesbare Syntax ausgedrückt
werden. Ich will da weder die Syntax von regulären Ausdrücken nutzen
noch dazu zwingen, Python-Syntax 1:1 zu nutzen.
Was ich mir vorstelle ist eine S-Expression-Syntax mit syntaktischem
Zucker:

    a | b | c -> (or a b c)
    a & b & c -> (and a b c)
    <zahl a>~<zahl b> -> (tol <zahl a> <zahl b>)
    <zahl a>..<zahl b> -> (inter <zahl a> <zahl b>)
    'abc' -> (literal 'abc')
    (@'X' a b c) -> (cap 'X' a b c)

Die Parser sollen per Default Whitespaces überspringen zwischen
den Parser-Teilausdrücken. (real 1.0) (real 2.0)(real 3.0)
passt also auf alle der folgenden Beispiele

    1.0 2.0 3.0
    1.0       2.0           3.0

Durch das Element (charwise ...) kann man aber erzwingen, dass er
keine Whitespaces überspringt

Capture-Gruppen lassen sich festlegen durch

    (@# a b c ...)       Unbenannte Gruppe (durch Index erreichbar)
    (@'X'# a b c ...)    Klassifizierte Gruppe. Matches für diese Gruppe sind
                         nummeriert
    (@'X' a b c ...)     Benannte Gruppe, darf nur einmal gematched werden

Referenziert werden können die Gruppen auf rechten Seiten von z.Bsp.
Substitutionals per \1 oder \'X' oder \'X'5

Wieso S-Expressions? Eine Listennotation mit Kommas oder Semikolon
hat den Nachteil, dass da Kommas stehen wo eigentlich standardmäßig
Leerzeichen stehen. Bei den S-Expressions dagegen stehen dort wirklich
Leerzeichen.

Wie parsen und verarbeiten wir diese Ausdrücke?

* Die Ausdrücke werden erst einmal stupide als S-Expressions geparst
* Dann wird jede S-Expression gegen einen Satz Patterns verglichen und
  gegebenenfalls ersetzt. So ein Pattern kann so aussehen:
