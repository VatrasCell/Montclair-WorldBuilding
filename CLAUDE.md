# Montclair-Worldbuilding

Worldbuilding-Wissensbasis für eine Fantasy-Welt (Dynastie Montclair), die auf einem privaten Minecraft-Server umgesetzt wird. Ersetzt einen bisherigen Workflow
über eine einzelne, endlos wachsende ChatGPT-Session + Google Docs. Alle Inhalte sind auf Deutsch.

## Struktur

- **`Kanon/`** — kurze, strukturierte **Fakten**. Erste Anlaufstelle für Kontext: hier vor jeder neuen Szene/jedem neuen Kapitel nachschlagen.
    - `Kanon/Welt/` — Weltereignisse (Große Verwüstung, Religion) und Orte außerhalb der Reiche (Halwyn)
    - `Kanon/Reiche/` — ein Steckbrief pro Königreich, inkl. `Status`-Feld (aktiv / zerstört / Herkunftsreich / unentwickelt); Montclair und Elmsworth zusätzlich mit `Stammbaum.md`,
      Montclair zusätzlich mit Orts- und Institutionsdateien (`Rat der Frauen.md`, `Hofrat.md`, `Fährwerder.md`)
    - `Kanon/Personen/Haus Montclair/` — ein Faktenblatt pro benannter Figur der Dynastie (Familie, Charakter, Lebensstationen, Tod, Status)
    - `Kanon/Personen/Haus Elmsworth/` — ein Faktenblatt pro benannter Figur der Elmsworther Dynastie; dazu `Kanon/Personen/Alfred der Gelehrte.md` und `Haus Thornfield.md`
- **`Werke/`** — die eigentliche **Prosa**, in-universe Texte: Königsbücher, Chroniken, Bauwerksberichte, Geschichten. Das ist der kreative Output, nicht die
  Faktenbasis.
- **`00-Meta/`** — Navigationshilfen: `Zeitleiste.md` (Generationenfolge und G-Achse), `Glossar.md` (A–Z-Index), `Offene-Fragen.md` (ungeklärte Kanon-Punkte),
  `Stilrichtlinien.md` (Ton je Werk-Typ und Namensregeln), `Konzepte/` (offene Entwurfsdokumente `Konzept-*.md` für noch nicht kanonreife Themen, siehe Arbeitsweise
  Punkt 3), `Archiv/` (alte Roh-Materialien und umgesetzte Konzepte, nicht mehr aktiv als Kontext nutzen).

## Arbeitsweise

1. **Fakten vor Prosa:** Neue kanonische Fakten (Geburt, Tod, Titel, Ereignis) zuerst in der passenden `Kanon/`-Datei festhalten, danach erst in `Werke/`
   ausformulieren. Das verhindert Widersprüche wie den behobenen „Adelaide von Winstone vs. Winthrope"-Fehler.
2. **Bei Unsicherheit:** In `00-Meta/Offene-Fragen.md` nachsehen bzw. dort ergänzen, statt Fakten zu erfinden. Fehlendes Wissen darf explizit als „nicht
   bekannt" markiert werden — das ist bei den zerstörten Reichen sogar erzählerisch beabsichtigt (siehe Weltregel unten).
3. **Konzept-Dokumente für noch grobe Themen:** Ist eine Idee noch nicht kanonreif (mehrere denkbare Richtungen, Details offen, reines Brainstorming) –
   z. B. ein neues System oder eine noch unausgearbeitete Facette eines Reichs –, zuerst ein Entwurfsdokument unter `00-Meta/Konzepte/Konzept-<Thema>.md`
   anlegen (Vorbild: `00-Meta/Konzepte/Konzept-Kartensystem.md`) und dort Ideen/Optionen offen sammeln, statt sie direkt und konkret in `Kanon/`-Dateien festzuschreiben.
   Erst nach Abstimmung mit dem Nutzer eine knappe, abschließende Fassung nach `Kanon/` übernehmen; Kanon-Dateien können auf das noch offene
   Konzept-Dokument verweisen, solange Details ausstehen. Ist ein Konzept vollständig in den Kanon übernommen, wird es als „umgesetzt" markiert und nach
   `00-Meta/Archiv/` verschoben.
4. **Neue Personen/Orte/Begriffe:** immer auch in `00-Meta/Glossar.md` eintragen.
5. **Stil:** siehe `00-Meta/Stilrichtlinien.md` — Königsbücher, Bauwerks-Chroniken, Aldrics Chronik und freie Geschichten haben je eigenen Ton.
6. **Vollständigkeits-Checkliste bei jedem neuen Kanon-Fakt** (Schnipzel einweben, offene Frage klären, Korrektur): immer alle folgenden Stellen
   durchgehen, nicht nur die naheliegendste Datei — jede wird bei Betroffenheit aktualisiert:
    - betroffene `Kanon/Personen/...`- bzw. `Kanon/Reiche/.../Steckbrief.md`-Datei(en)
    - `00-Meta/Glossar.md`
    - `00-Meta/Zeitleiste.md` (wird leicht vergessen, weil sie kein Fakten-, sondern ein Navigationsdokument ist — trotzdem bei jedem Ereignis mit
      zeitlicher Einordnung prüfen)
    - `00-Meta/Offene-Fragen.md`, falls der Fakt eine dort gelistete offene Frage klärt oder eine neue aufwirft
    - betroffene `Werke/`-Texte, falls der Fakt dort bereits (ggf. jetzt widersprüchlich) vorkommt
   Am zuverlässigsten: vor dem Editieren einmal repo-weit nach dem Namen der betroffenen Person/des Orts/Begriffs grep(en), statt die Liste der
   „relevanten Stellen" aus dem Gedächtnis zu schätzen.
7. **Vor Verwandtschafts- oder Chronologie-Aussagen** (wer ist wessen Vater/Großvater, was geschah vor/während/nach was) die entsprechende
   Kanon-Personendatei bzw. den Original-Werke-Text noch einmal gezielt lesen, statt sich auf die Erinnerung aus dem bisherigen Gesprächsverlauf zu
   verlassen — das hat in der Vergangenheit zu Fehlern geführt (z. B. „Großvater" statt „Vater", falsche zeitliche Einordnung von Ereignissen).
   Für die zeitliche Einordnung über Reichsgrenzen hinweg gilt die **G-Achse** (Generationsnummern, siehe `00-Meta/Zeitleiste.md`): Kind = +1, Geschwister und
   Ehepartner gleiche Generation, Herrschaft als Spanne. Sie ist rein kanonisch und kommt in den Werken nicht vor; „Jahre" und „Jahrhunderte" in Werken sind
   sprachliche Mittel.

## Zentrale Weltregeln

Die ersten drei Regeln (Erbfolge, Titel-Tradition, Sterbe-Tradition) sowie die Religionsregel sind bislang nur für **Montclair** kanonisch festgelegt, nicht
automatisch für die gesamte Welt. Andere Reiche können eigene, abweichende Traditionen haben oder ihre Regelungen sind schlicht noch nicht ausgearbeitet — das
sollte bei ihrer Ausarbeitung nicht stillschweigend als „gilt überall genauso" angenommen werden. Nur die Erinnerungsverlust-Regel ist explizit weltweit gültig
(sie beschreibt die Wirkung der Großen Verwüstung selbst).

- **Erbfolge (Montclair):** Seit Ferdinand III. gilt die Erstgeburts-Erbfolge (ältester Sohn erbt automatisch). Vorher war die Nachfolge nicht geregelt (Ursache
  des Streits nach Wilhelm I.). Ferdinand IV. ergänzte die Regel bei seiner Abdankung unter dem Druck des „Rats der Frauen": Existiert kein männlicher Erbe,
  erbt die älteste Tochter des Herrschers. Isabella I. bestätigte diese Ergänzung formell als dynastisches Recht.
- **Titel-Tradition (Montclair):** Ehefrauen von Königen erhalten nach der Hochzeit einen Adelstitel nach ihrem Herkunftsort (`von <Ort>`). Bei unbekannter
  Herkunft wird ein Reich stellvertretend zugeschrieben (Margarethe von Alden).
- **Sterbe-Tradition (Montclair, kulturell, nicht religiös verbindlich):** Über Generationen die Vorstellung, dass Ehefrauen ihren Männern rasch in den Tod
  folgen. Judith von Montclair durchbrach dies bewusst — mit gewaltsamen Konsequenzen.
- **Erinnerungsverlust durch die Große Verwüstung (weltweit):** Nicht jede In-Welt-Quelle kennt die Namen der durch die Katastrophe zerstörten Reiche (z. B.
  Aranthor). Das ist gewolltes Weltelement, kein zu behebender Widerspruch.
  Details: [Kanon/Welt/Die Große Verwüstung und die Westwanderung.md](Kanon/Welt/Die%20Große%20Verwüstung%20und%20die%20Westwanderung.md)
- **Elmsworth (eigene Regeln):** Erbfolge: erstgeborener Sohn, sonst ernennt der Adelsrat einen König aus der direkten Herrscherfamilie; die Königsfamilie trägt den
  Reichsnamen als Nachnamen; angeheiratete Frauen behalten einen Adelstitel, sonst „von Elmsworth". Details: [Kanon/Reiche/Königreich Elmsworth](Kanon/Reiche/Königreich%20Elmsworth/Steckbrief.md).
- **Religion (Montclairs Staatsreligion):** Der Monarch ist nicht das geistliche Oberhaupt der Staatsreligion. Andere Reiche können eigene Staatsreligionen mit
  eigenen Regeln haben, die aus derselben Fragment-Religion hervorgegangen sind. Details: [Kanon/Welt/Religion/](Kanon/Welt/Religion/)

## Aktueller Handlungsstand

Die Geschichte ist chronologisch bis einschließlich König **Wilhelm II. Montclair** (7. Generation) entwickelt; seine Herrschaft ist der aktuelle Schreibfokus
und noch nicht abgeschlossen (siehe [Kanon/Personen/Haus Montclair/Wilhelm II. Montclair.md](Kanon/Personen/Haus%20Montclair/Wilhelm%20II.%20Montclair.md)).
