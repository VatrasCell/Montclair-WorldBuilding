# Konzept: Karten und Bauwerke als lebender Teil des Kanons

Entwurfsdokument, noch nicht umgesetzt. Hält fest, wie Geografie und Bauwerks-Detail aus der parallel auf einem privaten Minecraft-Server gebauten
Welt in die bestehende Kanon/Werke-Struktur einfließen, ohne die Fallstricke reiner Bild-Screenshots zu übernehmen. Dient als Diskussionsgrundlage,
bevor Dateien angelegt oder `CLAUDE.md` erweitert werden.

## 1. Ausgangslage und Ziele

**Problem:** Karten liegen bisher nur als Xaeroworldmap-Screenshots vor, auf denen Ländergrenzen und Beschriftungen nachträglich eingezeichnet
werden.

- Bild als Kontext ist schlecht: handgemalte Overlays sind nur verlustbehaftet auswertbar, nicht durchsuchbar, nicht diffbar, nicht versionierbar.
- Geografie hat – anders als Personen/Ereignisse – eine externe Wahrheit: der Server verändert sich unabhängig davon, ob es im Kanon vermerkt wird
  (neue Siedlungen, verschobene Grenzen, neue Bauwerke). Ohne festen Mechanismus driftet der Kanon-Text lautlos vom tatsächlichen Weltstand ab.

**Ziele:**

- Text ist die kanonische Quelle für Geografie und Bauwerke – greifbar, grep-bar, versionierbar wie jede andere Kanon-Datei.
- Rohe Screenshots bleiben als Referenzmaterial erhalten, werden aber nicht direkt als Faktenquelle gelesen.
- Eine visuelle Darstellung (Karte) ist jederzeit aus dem Text ableitbar – nicht umgekehrt.
- Aktualisierung ist strukturell verankert (Teil der Vollständigkeits-Checkliste aus `CLAUDE.md`), nicht dem Erinnern im Einzelfall überlassen.
- Nachvollziehbarkeit über Zeit: erkennbar, wann welcher Geografie-/Bauwerks-Stand zuletzt bestätigt wurde.

**Nicht-Ziele:**

- Kein automatischer technischer Sync mit dem Server (kein Plugin, kein Weltexport, keine Live-Koordinaten-Pipeline). Der Server wird nicht vom
  Nutzer administriert – jede Lösung muss rein clientseitig funktionieren, ohne Mitwirkung der Serveradministration.
- Keine exakte Block-für-Block-Vermessung – Genauigkeit nur so weit, wie sie erzählerisch/kartografisch relevant ist.
- Keine Ablösung der Screenshots – sie bleiben als Referenzbild bestehen, verlieren nur ihre Rolle als alleinige Faktenquelle.

## 2. Architektur: drei Schichten, vier Rohdatenquellen

1. **Rohmaterial** – unbearbeitete, datierte Bild-/Textdaten, reine Referenz, nie direkt als Faktenquelle gelesen. Vier technisch sehr
   unterschiedliche Quellen (Details in Abschnitt 3):

   | Quelle | Koordinatenbezug | Liefert |
   |---|---|---|
   | Kachel-Export (PNG) | exakt, 1 Pixel = 1 Block | Landschaftsbild |
   | POI-Wegpunkte (`worldbuilding`-Set) | exakt (x/y/z) | benannte Orte/Bauwerke |
   | Grenz-Wegpunkte (Set `worldbuilding_borders`) | exakt (x/y/z) | Reichsgrenzen als Punktkette |
   | Isometrische Detailbilder | keiner (freie Kamera) | Architektur-/Baudetail |

2. **Kanon-Text** – die eigentliche Wahrheit: `Kanon/Welt/Geographie.md`, die „Standort"-Abschnitte der Reiche-Steckbriefe,
   `Werke/Bauwerke-Chroniken/`.
3. **Abgeleitete Visualisierung** – bei Bedarf aus (2) generierte, vereinfachte Karte (z. B. als Artifact), rein zur Kontrolle/Anschauung, kein
   Kanon für sich genommen.

## 3. Die vier Rohdatenquellen im Detail

### 3.1 Xaero-Wegpunkte (POIs)

Format bestätigt anhand echter Daten (`mw$default_2.txt`):
`waypoint:name:initials:x:y:z:color:disabled:type:set:rotate_on_tp:tp_yaw:visibility_type:destination` – selbstdokumentiert, Doppelpunkt-getrennt,
trivial zu parsen. Alle Wegpunkt-Sets liegen zusammen in einer Datei pro Dimension; unterschieden über die `set`-Spalte, deklariert in einer
`sets:`-Kopfzeile.

**Clutter-Problem gelöst:** ein eigenes Set `worldbuilding` trennt Kanon-Marker von normalen Spiel-Landmarken; `disabled:true` macht sie auf der
Minimap unsichtbar, bleibt aber für den Parser (der die Rohdatei liest, nicht die gerenderte Karte) vollständig auswertbar. Damit ist die Zahl der
Marker praktisch unbegrenzt, ohne beim Spielen zu stören.

**Kategorisierung über `color`:** bereits in Nutzung als Reichs-Referenz – `color:11` (Türkis) für alle Montclair-Marker, deckt sich mit den
kanonischen Reichsfarben „Schwarz, Weiß, Cyan" laut [Steckbrief](../../Kanon/Reiche/Königreich%20Montclair/Steckbrief.md). `color` ist kein freier
Wert, sondern einer von **21 festen Xaero-Farb-IDs** (0–20) – die IDs 0–15 entsprechen den 16 Standard-Minecraft-Textfarben, 16–20 sind zusätzliche
Xaero-eigene Farben. Vollständige Palette, vom Nutzer per Referenz-Wegpunkten ermittelt (Set `colors`, Stand 2026-08-16):

| ID | Farbe | ID | Farbe | ID | Farbe |
|---|---|---|---|---|---|
| 0 | schwarz | 7 | grau | 14 | gelb |
| 1 | dunkelblau | 8 | dunkelgrau | 15 | weiß |
| 2 | dunkelgrün | 9 | blau | 16 | magenta |
| 3 | dunkeltürkis | 10 | grün | 17 | hellblau |
| 4 | dunkelrot | 11 | **türkis (Montclair)** | 18 | hellgrün |
| 5 | dunkelviolett | 12 | rot | 19 | pink |
| 6 | gold | 13 | violett | 20 | braun |

**Zuordnung Reich↔Farbe (Stand 2026-10-03):** Montclair `color:11` (Türkis), Elmsworth `color:12` (Rot, passend zu den Reichsfarben „Rot, Gelb"). Das
Skript führt sie in `REICH_COLORS` (`tools/kartenimport.py`). Die vollständige Zuordnungstabelle wird ergänzt, sobald weitere Reiche Marker bekommen – mit
der vollständigen Palette bereits bekannt, ist das jetzt nur noch eine Zuordnungs-, keine Recherchefrage mehr (s. offene Frage unten). Bei
POI-Wegpunkten (`worldbuilding`) bleibt `initials` freier Anfangsbuchstabe ohne feste Bedeutung; bei Grenz-Wegpunkten (`worldbuilding_borders`) trägt
`initials` dagegen die **Grenz-ID** – s. Abschnitt 3.3.

**Echter Datenstand geprüft** (Stand 2026-08-12): 13 Marker im `worldbuilding`-Set, alle kanon-zuordenbar – Burg Montclair, Burg Wilhelmshöhe,
Stadt/Palast/Universität/Stadtkirche/Diplomatenviertel Montclair, Felder, Dorf 1–3, sowie **Kloster** (1009|65|-10677). Damit ist die bisher offene
Frage nach dem Ort von Wilhelms II. Kloster geklärt (nur der Eigenname bleibt offen, s. `Offene-Fragen.md`). Grenzpunkte kommen in den echten Daten
noch nicht vor.

### 3.2 Kachel-Export (Landschaft)

Xaero exportiert die Karte über die Export-Funktion als **Raster einzelner Kachel-PNGs**, Dateiname trägt direkt die Koordinate:
`{Spalte}_{Zeile}_x{X}_z{Z}.png`. Verifiziert am Testexport (`map exports/2026-08-13_21.36.56/`, 173+ Kacheln): jede Kachel exakt 1024×1024 Pixel,
Koordinatenschritt zwischen Kacheln ebenfalls exakt 1024 Blöcke, Spalte→x und Zeile→z unabhängig/orthogonal. Damit gilt **1 Pixel = 1 Block**,
exakt, ohne Bildanalyse oder manuelle Kalibrierung – reines Parsen des Dateinamens. (Eine frühere OCR-Idee, basierend auf der Annahme fehlender
Koordinaten-Metadaten, ist damit hinfällig, ebenso die Voraussetzung „Wegpunkte müssen beim Export sichtbar sein".)

**Scope-Filterung:** da nur ein Bruchteil der Server-Karte zur Montclair-Welt gehört, wird die relevante Bounding Box nicht manuell gepflegt,
sondern automatisch aus der Vereinigung aller rekonstruierten Reichsgrenzen (s. 3.3) abgeleitet. Nur Kacheln, die diese Box überschneiden, werden
per Dateinamen-Arithmetik ausgewählt und nach `Assets/Karten/<scope>/` kopiert – der Rest bleibt im lokalen Export-Ordner des Nutzers.

### 3.3 Grenz-Wegpunkte (Reichsgrenzen)

Xaero kennt nur Punkte, keine Flächen oder Linien. Gewählte Lösung: ein zweites Wegpunkt-Set, **`worldbuilding_borders`**, das dieselben
Set-/`disabled`-Mechanismen wie `worldbuilding` nutzt und ebenfalls über `color` je Reich unterschieden wird – kein zusätzlicher Mod, löst das
Clutter-Problem auch hier.

**Rekonstruktion über explizite Nummerierung – Namenskonvention (Stand 2026-08-17):** ursprünglich wurde die Reihenfolge der Grenzpunkte rein
geometrisch rekonstruiert (erst „nächste-Nachbarn", dann Greedy-Tour + 2-opt, s. u.). Beides ist jetzt überflüssig: `initials` trägt die
**Grenz-ID** (z. B. `A`), `name` die Grenz-ID plus eine **aufsteigende Nummer** (`A1`, `A2`, … `A22`). Die Reihenfolge entlang der Grenze steht damit
direkt in den Daten – der Nutzer setzt die Wegpunkte im Spiel einfach der Reihe nach und nummeriert sie durch, kein zusätzliches Werkzeug nötig. Das
Skript gruppiert die Grenzpunkte eines Reichs (gleiche `color`) nach `initials`, sortiert jede Gruppe numerisch nach der Zahl in `name` und
verbindet sie in dieser Reihenfolge zu einer geschlossenen Fläche. Eine Selbstüberschneidung wird weiterhin geprüft (Ray-Casting/CCW-Segmenttest)
und führt zu einem Fehler statt stillschweigender Weiterverarbeitung – jetzt aber als echtes Warnsignal für eine falsch vergebene Nummer im Spiel,
nicht mehr als Grenzfall eines geometrischen Heuristik-Verfahrens. Ebenso werden doppelt vergebene Nummern innerhalb einer Grenz-ID erkannt und
gemeldet.

**Zwischenpunkte (Stand 2026-10-01):** Nachträglich eingefügte Punkte erhalten einen Punkt-Suffix, ohne die übrige Nummerierung zu ändern:
`A15.1`, `A15.2` liegen zwischen `A15` und `A16`; weiter verschachtelt geht es mit `A15.1.1` (zwischen `A15.1` und `A15.2`). Sortiert wird numerisch
je Segment (`A15` < `A15.1` < `A15.2` < `A15.10` < `A16`), Duplikate werden wie bisher gemeldet. Das macht Verläufe erweiter- und editierbar, ohne
im Spiel alle Folgepunkte umzubenennen.

**Mehrere Grenzflächen pro Reich:** verschiedene Grenz-IDs mit derselben `color` (z. B. `A1…An` für das Kernland, `B1…Bm` für eine Insel oder
Exklave) ergeben mehrere getrennte, unabhängig voneinander rekonstruierte Flächen desselben Reichs – für die Kachel-Auswahl (Abschnitt 3.2) wird
einfach die Vereinigung aller Flächen verwendet.

Die frühere Greedy-Tour-+-2-opt-Lösung (die ihrerseits die noch frühere „nächste-Nachbarn"-Methode ablöste, welche am echten 22-Punkte-Datensatz mit
einer falschen „mehrdeutige Nachbarschaft"-Meldung scheiterte) ist damit obsolet, ebenso die zuvor dokumentierte Einschränkung zur lokalen
Reihenfolge-Mehrdeutigkeit dichter Punktgruppen: mit expliziter Nummerierung gibt es keine Mehrdeutigkeit mehr, unabhängig davon, wie dicht
Grenzpunkte beieinanderliegen.

Mit den echten, jetzt durchnummerierten 22 `worldbuilding_borders`-Wegpunkten (Grenz-ID `A`) über das v1-Skript (Abschnitt 8) liefert die
Rekonstruktion weiterhin **dieselbe** Kachel-Auswahl wie beim früheren XaeroPlus-Testumriss (s. Abschnitt 9) und der vorherigen
Greedy-Tour-+-2-opt-Rekonstruktion: von 173+ exportierten Kacheln überschneiden genau 7 die Montclair-Grenze (`6_6`, `6_7`, `6_8`, `7_6`, `7_7`,
`7_8`, `8_7` – zwei davon ohne eigenen POI, nur am Grenzrand berührt).

### 3.4 Isometrische Detailbilder (Bauwerke)

Vierte, andersartige Quelle: frei aufgenommene isometrische Screenshots einzelner Bauwerke (freie Kamera/Zoom, z. B. Creative-Flug), kein
Top-Down-Export. Erster Fund: vier Aufnahmen von Burg Wilhelmshöhe unter `Assets/Reiche/Montclair/Burg Wilhelmshöhe/`.

- **Kein Koordinatenbezug** – anders als der Kachel-Export gibt es keine automatische Kalibrierung; diese Ebene ist reines Rohmaterial, nie
  Rechengrundlage.
- **Dafür weit höherer Detailgrad** – Turmformen, Dächer, Fassadenmaterial, Fensterformen, Bannerfarben, angrenzende Bauten, die aus der
  Vogelperspektive prinzipiell unsichtbar bleiben, unabhängig von der Export-Auflösung.
- **Ordnungsprinzip:** ein Unterordner pro Bauwerk unter `Assets/Reiche/<Reich>/<Bauwerksname>/`, passend zur bestehenden Konvention für
  Reichs-Assets (bisher Flaggen/Wappen direkt unter `Assets/Reiche/<Reich>/`).

## 4. Auswertungsmethode: zwei Ebenen

Jede Bildauswertung – Kachel-PNG wie isometrisches Detailbild – läuft in zwei Schritten:

- **Ebene A – Minecraft-Ebene („Was sehe ich?"):** rein technische Beschreibung des Screenshots – Blocktypen, Bauformen, Farben, Anordnung,
  inklusive Unsicherheit, wo sie besteht. Beschreibt das Spiel, noch nicht die Welt.
- **Ebene B – narrative Ebene („Was bildet das im Kontext dieses Worldbuilding-Projekts ab?"):** die kanonrelevante Übersetzung von Ebene A in
  Weltbegriffe – aus „Spitzbogenfenster mit Buntglas, Strebepfeiler" wird z. B. „ein der Burg angegliederter Sakralbau". **Nur Ebene B geht in
  Kanon-Texte ein.**

Ebene B ergibt sich aus Ebene A, nicht umgekehrt: jede Aussage muss auf eine konkrete Beobachtung zurückführbar sein, statt frei erfunden zu
werden. Wo Ebene A unsicher bleibt, bleibt Ebene B entsprechend vorsichtig formuliert oder offen, statt die Unsicherheit stillschweigend in eine
sichere Kanon-Aussage zu übersetzen. Eine neue Ebene-B-Erkenntnis ist wie jeder andere neue Kanon-Fakt zu behandeln (Fakten-vor-Prosa aus
`CLAUDE.md`): erst im Steckbrief/in der Bauwerks-Chronik festhalten, bevor sie in weiteren Werke-Texten vorausgesetzt wird.

**Zwei Praxistests bereits durchgeführt:**

- **Landschafts-Kachel `7_7_x512_z-10240.png` (2026-08-13):** Kalibrierung empirisch bestätigt (Burg Wilhelmshöhe und Burg Montclair exakt an
  vorhergesagten Pixel-Positionen gefunden; Achsen-Orientierung damit geklärt: Norden oben, Westen links, Standardausrichtung). Detailgrad-Grenze
  erprobt: Biom-/Blocktyp-Vermutungen („mit Minecraft-Brille") funktionieren, sind aber ohne Zoom auf Blockebene unsicher bei farblich ähnlichen
  Kandidaten (Dark Forest vs. Taiga, Cobblestone vs. Steinziegel vs. Andesit) – s. offene Frage unten.
- **Isometrische Bilder von Burg Wilhelmshöhe (2026-08-16):** Ebene-A-Beschreibung (mehrtürmige Burg, separater kirchenartiger Anbau mit
  Buntglasfenstern und Strebepfeilern, ein stilistisch älterer Fachwerkturm, Lage auf schneebedecktem Gipfel) ergab auf Ebene B den einzigen
  kanonrelevanten Befund dieses Tests: **Burg Wilhelmshöhe besitzt vermutlich einen eigenen Sakralbau (Kapelle/Kathedrale), bislang in keinem
  Kanon-Text erwähnt.** Eine zweite Beobachtung (möglicher älterer Baukern am Fachwerkturm) wurde bewusst als Hypothese markiert, nicht als Fakt.
  Beide Ergebnisse sind noch nicht in den Kanon übernommen – ausstehende Nutzer-Entscheidung.

## 5. Zusammenführung zu generierten Daten

POI-Set und Grenzen-Set tragen beide `color` als Reichs-Kennung – der Merge ist ein einfacher Join über `color`/Reich, komplett in echten
Koordinaten, ohne jede Kalibrierung. Pro Reich landen POIs und die rekonstruierte Grenzfläche in einem gemeinsamen, generierten Datensatz (s.
Abschnitt 6). Landschafts- und Detailbilder werden separat behandelt, da sie bildbasiert sind (s. Abschnitt 4) statt strukturiert.

## 6. Dateistruktur

- `Kanon/Welt/Geographie.md` – zentrale Welt-Ebene: Lagebeziehungen zwischen Reichen, Distanzen, Koordinaten-Anker, natürliche Grenzen.
- Bestehende „Standort"-Abschnitte in `Kanon/Reiche/.../Steckbrief.md` bleiben die Detailebene pro Reich, ggf. um Verweise auf `Geographie.md`
  ergänzt.
- `Assets/Karten/Wegpunkte.txt` – vollständige Kopie der Xaero-Wegpunkt-Datei (1:1, alle Sets – bewusst komplett committet statt gefiltert), liegt
  übergeordnet (nicht scope-spezifisch, da eine Datei alle Reiche enthält) und wird bei jeder Abholung überschrieben. Keine Datums-Unterordner –
  Versionierung/Historie läuft über git, nicht über parallele Snapshot-Ordner.
- `Assets/Karten/<scope>/` (z. B. `Assets/Karten/montclair/`) – die für diesen Scope relevanten Kachel-PNGs (Dateinamen unverändert). Wird bei
  jeder Abholung desselben Scopes komplett neu geschrieben (Ordner vorher geleert, damit keine inzwischen irrelevanten Alt-Kacheln liegen bleiben)
  – auch hier Versionierung über git statt über Datums-Unterordner.
- `Assets/Reiche/<Reich>/<Bauwerksname>/` – isometrische Detailbilder je Bauwerk (Dateinamen nach Aufnahmezeitpunkt).
- `00-Meta/Kartendaten/welt.generiert.json` – struktureller Merge aus POIs + Grenzflächen (Abschnitt 5), nie von Hand editiert, nie Ersatz für
  `Geographie.md`.

## 7. Format von `Geographie.md` (Entwurf)

- Pro Reich/Region ein kurzer Block: Lage relativ zu Nachbarn, ungefähre Distanz/Reisezeit, Grenzverlauf in Textform, Datum der letzten
  Bestätigung.
- Ein Änderungs-Log-Abschnitt (nach dem Vorbild von `Offene-Fragen.md`s „Geklärt"-Historie): Datum + was sich geändert hat + auslösendes
  Ereignis/Bauwerk.
- Zerstörte/unbekannte Reiche (Aranthor etc.) werden bewusst nicht präzise verortet – passend zur Erinnerungsverlust-Weltregel; „nicht bekannt"
  ist hier ein zulässiger, sogar beabsichtigter Zustand.

## 8. Pipeline und Update-Workflow

**Erste Ausbaustufe (v1-Skript, `tools/kartenimport.py`) – umgesetzt und gegen echte Daten erfolgreich getestet (2026-08-16):** ein manuell
aufgerufenes Python-Skript, Scope über CLI-Argument, vorerst auf Reich-Ebene (`--scope montclair`). Deckt nur das Holen der Rohdaten ab
(Pipeline-Schritte 1–3 unten in vereinfachter Form), noch **kein** struktureller Merge (Schritt 4) und keine Auswertung (Schritt 6) – das folgt in
einer späteren Ausbaustufe. Ein echter Lauf gegen die reale Wegpunkt-Datei und den realen Kachel-Export lieferte die in Abschnitt 3.3 dokumentierten
7 Kacheln, identisch zum früheren XaeroPlus-Testergebnis. Seit 2026-10-03 gilt `--scope elmsworth` (25 Grenzpunkte der Grenz-ID `A`, `color:12`, ebenfalls
7 Kacheln).

1. Kopiert die aktuelle Xaero-Wegpunkt-Datei vollständig (alle Sets, ungefiltert) nach `Assets/Karten/Wegpunkte.txt` – überschreibt eine
   vorhandene Datei, keine Datums-Unterordner (Historie über git).
2. Rekonstruiert aus dem `worldbuilding_borders`-Set die Grenzfläche(n) des per `--scope` gewählten Reichs anhand der Grenz-ID/Nummerierung in
   `initials`/`name` (s. Abschnitt 3.3) – mehrere Grenz-IDs ergeben mehrere Flächen (Exklaven).
3. Ermittelt den aktuellsten Export-Unterordner unter einem im Skript konfigurierbaren Basispfad (z. B. `.../map exports/`) – die Unterordner
   sind bereits datumsbenannt, das Skript nimmt automatisch den jüngsten.
4. Kopiert daraus nur die Kacheln, die die Grenzfläche aus Schritt 2 überschneiden, nach `Assets/Karten/<scope>/` – der Ordner wird vorher
   geleert, damit bei einer neuen Abholung keine inzwischen irrelevanten Alt-Kacheln liegen bleiben.

Der volle 7-Schritt-Ablauf unten bleibt das Zielbild; die v1-Ausbaustufe ist ein bewusst kleinerer erster Schnitt davon.

1. **Raster-Export:** Export aus Xaero über die Kachel-Export-Funktion (kein bekannter Automatisierungs-Hook) → lokaler Export-Ordner des
   Nutzers.
2. **Wegpunkt-Export:** Skript liest die Waypoints-Datei, filtert auf `set == worldbuilding`, löst `color` über die Reichs-Zuordnungstabelle auf.
3. **Grenzen-Export:** dasselbe Skript filtert zusätzlich auf das Grenzen-Set, rekonstruiert je Grenz-ID (Gruppierung über `initials`, Reihenfolge
   über die Nummer in `name`) eine geschlossene Fläche und validiert (überschneidungsfrei, keine doppelten Nummern – sonst Fehlermeldung statt
   stillschweigender Weiterverarbeitung). Die Vereinigung aller Flächen (auch über mehrere Grenz-IDs/Exklaven je Reich hinweg) ergibt automatisch
   die relevante Bounding Box.
4. **Struktureller Merge:** POIs und Grenzfläche werden über `color`/Reich zu `00-Meta/Kartendaten/welt.generiert.json` zusammengeführt.
5. **Kachel-Auswahl:** nur Kacheln, die die Bounding Box aus Schritt 3 überschneiden, werden per Dateinamen-Parsing nach
   `Assets/Karten/<scope>/` kopiert – reine Koordinaten-Arithmetik, keine Bildanalyse.
6. **Landschafts-/Detail-Auswertung:** Zwei-Ebenen-Methode (Abschnitt 4) auf übernommene Kacheln bzw. neue isometrische Bilder angewendet, fließt
   inhaltlich in `Geographie.md` bzw. die betroffene Bauwerks-Chronik/den Steckbrief ein.
7. **Kanon-Abgleich:** `Geographie.md` bleibt die von Hand/KI kuratierte Prosa-Wahrheit, verweist auf bzw. fasst die generierten Daten (Schritt 4)
   und die Auswertung (Schritt 6) zusammen, wird aber **nie** automatisch überschrieben – ein Export-Lauf darf keine sorgfältig formulierten
   Kanon-Texte zerstören. Ein `git diff` zwischen zwei generierten Ständen zeigt dabei bereits automatisch, was sich geografisch verändert hat,
   bevor überhaupt jemand die Prosa anfasst – das ist der technische Kern des „lebender Kanon"-Ziels.

**Zwei Auslöser, die eine Aktualisierung erzwingen statt sie dem Zufall zu überlassen:**

1. **Neuer Kanon-Fakt mit räumlicher Wirkung** (neue Siedlung, Grenzverschiebung, Bauwerk): `Geographie.md` wird ein weiterer Pflichtpunkt in der
   Vollständigkeits-Checkliste aus `CLAUDE.md`, gleichrangig mit `Zeitleiste.md`.
2. **Neuer Screenshot wird eingespielt** (Kachel oder isometrisch): aktiver Abgleich gegen den aktuellen `Geographie.md`-Stand statt bloßes
   Ablegen – Unstimmigkeiten werden explizit rückgefragt, bevor der Text angepasst wird.

Eine generierte Visualisierung wird nicht bei jeder Änderung zwingend neu erzeugt, sondern nur, wenn eine sichtbare Kontrolle gewünscht ist. Das
Parser-Skript selbst hätte im Repo Platz (z. B. `tools/kartenimport.py`), müsste aber **lokal vom Nutzer** ausgeführt werden, sobald die Rohdaten
im Projektordner liegen – Claude Code hat keinen Zugriff auf den Minecraft-Client-/Server-Rechner.

## 9. Geprüft und verworfen

- **XaeroPlus „Drawing"-Feature:** technisch erfolgreich getestet (s. Abschnitt 3.3), aber verworfen – keine Set-/Sichtbarkeits-Zuordnung für
  Drawings (das Clutter-Problem, das für Wegpunkte gelöst wurde, bliebe für Grenzen ungelöst), keine echten Flächen gegenüber einer Punktkette
  (die Fläche entsteht ohnehin erst rechnerisch), und ein unverhältnismäßiger Fußabdruck (Anarchie-Server-Mod mit FPS-Optimierung,
  Chunk-Highlighting, Baritone-Integration) für den eigentlichen Bedarf.
- **Eigene, schlanke Mod-Erweiterung auf XaeroPlus-Basis:** erwogen, um nur das fehlende Set-/Sichtbarkeits-Feature zu ergänzen (MIT-Lizenz
  erlaubt Wiederverwendung). Realitätscheck im Quellcode: `Drawing.java`/`DrawingCache.java`/`DrawingDatabase.java` allein ca. 2.400 Zeilen von
  ~6.200 Gesamtzeilen, dazu eigene Rendering-Klassen und mindestens 3 Mixin-Klassen in Xaeros undokumentierte interne API. Kein
  Skript-Wochenende, sondern ein echtes Fabric/Forge-Modding-Projekt mit laufendem Pflegeaufwand – nicht als aktiver Kandidat aufgenommen.
- **OCR-basierte Pixel-Kalibrierung:** ursprünglich für nötig gehalten (basierend auf
  [MCMapCropper](https://github.com/SeriousGuy888/MCMapCropper), einem Drittanbieter-Tool für dasselbe Problem), durch die Entdeckung der
  koordinatentragenden Kachel-Dateinamen (Abschnitt 3.2) vollständig ersetzt.
- **Lokaler Grenz-Editor über dem PNG-Export** (HTML/Canvas-Werkzeug zum Grenzen-Abklicken): als Alternative zu Wegpunkt-Ketten dokumentiert,
  falls weichere Grenzverläufe später gewünscht werden. Aktuell nicht die erste Wahl, aber nicht endgültig gestrichen – s. offene Frage unten.

## 10. Offene Fragen an den Nutzer

- Granularität: Reicht eine relative Beschreibung („im Osten, drei Tagesreisen entfernt") oder sollen echte Minecraft-Koordinaten hinterlegt
  werden?
- Sollen zerstörte/unentdeckte Reiche überhaupt einen Geographie-Eintrag bekommen, oder bewusst ausgespart bleiben?
- Umfang der ersten Visualisierung: nur der bereits ausgearbeitete Montclair-Kontinent, oder gleich ein Weltüberblick mit den Lücken der
  unbekannten Reiche?
- Wie wird mit noch nicht kanonisch benannten Bauten auf einem neuen Screenshot umgegangen (z. B. erst als offene Frage vormerken, bevor sie in
  `Geographie.md` landen)?
- Mit der vollständigen 21-Farben-Palette bekannt (s. Abschnitt 3.1): sollen die übrigen 20 Farben den bereits kanonisch benannten Reichen
  (Winthrope, Elmsworth, Alden, Penworth, Lythoria, Caerthun, Varenheim, den zerstörten Reichen etc.) schon jetzt fest zugeordnet werden, oder
  weiterhin erst dann, wenn dort tatsächlich Marker gesetzt werden?
- Soll der lokale Grenz-Editor trotz der Festlegung auf Wegpunkt-Ketten als Fallback im Konzept bleiben, oder ganz gestrichen werden?
- Landschafts-Auswertung des PNG: reicht eine freie Beschreibung in Prosa, oder soll das strukturierter erfasst werden (z. B. grobe
  Terrain-Kategorien pro Teilgebiet)?
- **Erzielbarer Detailgrad der Landschafts-Auswertung:** Biom-/Blocktyp-Vermutungen sind ohne Zoom auf Blockebene unsicher bei farblich ähnlichen
  Kandidaten (z. B. Dark Forest vs. Old-Growth-Taiga, Cobblestone vs. Steinziegel vs. Andesit). Wie soll damit umgegangen werden – unsichere
  Zuordnungen explizit als „vermutlich"/„nicht sicher unterscheidbar" kennzeichnen, ganz weglassen, oder reicht die grobe Einordnung
  („Waldgebiet", „Gebirge") ohne Biom-Namen?
- Export-Kadenz: nach jeder Bausession, nur bei kanonrelevanten Änderungen, oder festes Intervall?
- Isometrische Detailbilder: sollen sie künftig verbindlich pro fertiggestelltem Bauwerk angelegt werden (analog zur Bauwerks-Chronik als
  Werke-Text), oder bleiben sie ein optionales Extra, das nur gelegentlich entsteht?
- Konkret zum Burg-Wilhelmshöhe-Praxistest (Abschnitt 4): soll der Sakralbau-Befund (Kapelle/Kathedrale) als neuer Kanon-Fakt übernommen werden?

## 11. Nächste Schritte (falls das Konzept so freigegeben wird)

1. `Kanon/Welt/Geographie.md` anlegen, erste Bestandsaufnahme aus den bereits vorhandenen „Standort"-Absätzen der Reiche-Steckbriefe destillieren.
2. `Assets/Karten/` anlegen, aus dem vorhandenen Testexport (`map exports/2026-08-13_21.36.56/`) die für Montclair relevanten Kacheln datiert
   einordnen.
3. CLAUDE.md-Checkliste (Punkt 5) um `Geographie.md` erweitern.
4. ~~Richtwert für den maximalen Abstand zwischen benachbarten Grenz-Wegpunkten festlegen~~ – durch die Nummerierungs-Konvention
   (Grenz-ID/aufsteigende Nummer in `initials`/`name`, Abschnitt 3.3) obsolet: die Reihenfolge steht direkt in den Daten, kein Abstandsrichtwert
   und keine geometrische Rekonstruktion mehr nötig.
5. ~~v1-Skript bauen~~ – **erledigt** (`tools/kartenimport.py`), erfolgreich gegen echte Daten getestet (22 nummerierte Grenzpunkte,
   7-Kachel-Auswahl, identisch zum früheren XaeroPlus-Testergebnis; unterstützt jetzt auch mehrere Grenzflächen pro Reich für Exklaven).
6. Eines der beiden bereits erfolgreich getesteten Auswertungsergebnisse (Landschafts-Kachel oder Burg-Wilhelmshöhe-Sakralbau) tatsächlich in
   `Geographie.md` bzw. einen Steckbrief/eine Bauwerks-Chronik übernehmen – erster echter Kanon-Fakt aus dieser Pipeline.
7. Ordnungsprinzip für isometrische Detailbilder final festlegen (offene Frage oben) und bei weiteren fertiggestellten Bauwerken anwenden.
8. v1-Skript um den strukturellen Merge (POIs + Grenzfläche, Abschnitt 5) erweitern – nächste Ausbaustufe nach Abschnitt 8.
