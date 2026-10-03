"""v1: Wegpunkte + Grenz-Kacheln eines Reichs aus Xaero's World Map ins Projekt kopieren.

Siehe 00-Meta/Konzepte/Konzept-Kartensystem.md, Abschnitt 8 ("Erste Ausbaustufe"). Deckt nur das Holen der
Rohdaten ab -- kein struktureller Merge, keine Auswertung. Muss lokal beim Nutzer laufen, da der
Minecraft-Client-Ordner und der Kachel-Export außerhalb des Repos liegen.

Aufruf: python tools/kartenimport.py --scope montclair
"""

import argparse
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_env(path):
    # Minimaler .env-Parser (KEY=VALUE, '#'-Kommentare, optionale Anführungszeichen) -- bewusst
    # ohne Zusatzabhängigkeit. Bereits gesetzte Umgebungsvariablen haben Vorrang.
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def _require_env(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(
            f"Umgebungsvariable {name} fehlt -- in {REPO_ROOT / '.env'} setzen "
            f"(Vorlage: .env.example)."
        )
    return value


# --- Lokale Konfiguration: liegt in der nicht eingecheckten .env (siehe .env.example) ---
_load_env(REPO_ROOT / ".env")

REICH_COLORS = {
    "montclair": 11,
}
BORDER_SET = "worldbuilding_borders"
TILE_SIZE = 1024
TILE_NAME_RE = re.compile(r"^\d+_\d+_x(-?\d+)_z(-?\d+)\.png$", re.IGNORECASE)
# Konvention für Grenz-Wegpunkte: initials = Grenz-ID (erlaubt mehrere Grenzflächen pro Reich,
# z. B. für Exklaven/Inseln), name = Grenz-ID + aufsteigende Nummer (z. B. "A1", "A2", ...). Die
# Nummer liefert die Reihenfolge entlang der Grenze direkt aus den Daten -- keine geometrische
# Rekonstruktion mehr nötig. Zwischenpunkte werden mit Punkt-Suffix eingefügt (z. B. "A15.1",
# "A15.2" liegen zwischen A15 und A16, "A15.1.1" zwischen A15.1 und A15.2), ohne umzunummerieren.
BORDER_NUMBER_RE = re.compile(r"(\d+(?:\.\d+)*)$")

KARTEN_DIR = REPO_ROOT / "Assets" / "Karten"
WAYPOINTS_DEST = KARTEN_DIR / "Wegpunkte.txt"


class BoundaryError(Exception):
    pass


def parse_waypoint_file(path):
    waypoints = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("waypoint:"):
                continue
            parts = line.split(":")
            if len(parts) < 10:
                continue
            _, name, initials, x, y, z, color, disabled, wtype, set_ = parts[:10]
            waypoints.append({
                "name": name,
                "initials": initials,
                "x": int(x),
                "z": int(z),
                "color": int(color),
                "set": set_,
            })
    return waypoints


def _find_self_intersection(polygon):
    n = len(polygon)
    edges = list(zip(polygon, polygon[1:] + polygon[:1]))
    for i in range(n):
        for j in range(i + 1, n):
            if j == i or (i + 1) % n == j or (j + 1) % n == i:
                continue
            if segments_intersect(edges[i][0], edges[i][1], edges[j][0], edges[j][1]):
                return i, j
    return None


def _order_by_number(grenz_id, points):
    numbered = []
    for p in points:
        m = BORDER_NUMBER_RE.search(p["name"])
        if not m:
            raise BoundaryError(
                f"Grenzpunkt '{p['name']}' (Grenz-ID '{grenz_id}') folgt nicht dem Namensschema "
                f"<Grenz-ID><Nummer>, z. B. A1 oder A15.1 -- Wegpunkt im Spiel prüfen."
            )
        # Tupel-Vergleich: (15,) < (15, 1) < (15, 2) < (15, 10) < (16,)
        numbered.append((tuple(int(part) for part in m.group(1).split(".")), p))
    numbered.sort(key=lambda t: t[0])

    numbers = [n for n, _ in numbered]
    if len(set(numbers)) != len(numbers):
        dupes = sorted(".".join(map(str, n)) for n in {n for n in numbers if numbers.count(n) > 1})
        raise BoundaryError(
            f"Grenz-ID '{grenz_id}': Nummer(n) {dupes} mehrfach vergeben -- Nummerierung im Spiel prüfen."
        )
    return [p for _, p in numbered]


def reconstruct_boundaries(border_points):
    # Konvention: initials = Grenz-ID, name = Grenz-ID + aufsteigende Nummer (z. B. "A1"..."A22").
    # Die Nummer liefert die Reihenfolge entlang der Grenze direkt -- keine geometrische
    # Rekonstruktion mehr nötig. Mehrere Grenz-IDs pro Reich (gleiche color) ergeben mehrere
    # getrennte Flächen, z. B. für Exklaven/Inseln.
    groups = defaultdict(list)
    for p in border_points:
        groups[p["initials"]].append(p)

    boundaries = {}
    for grenz_id, points in sorted(groups.items()):
        ordered = _order_by_number(grenz_id, points)
        if len(ordered) < 3:
            raise BoundaryError(
                f"Grenz-ID '{grenz_id}' hat nur {len(ordered)} Punkt(e) -- mindestens 3 nötig für eine Fläche."
            )

        polygon = [(p["x"], p["z"]) for p in ordered]
        crossing = _find_self_intersection(polygon)
        if crossing:
            i, j = crossing
            n = len(ordered)
            a, b = ordered[i], ordered[(i + 1) % n]
            c, d = ordered[j], ordered[(j + 1) % n]
            raise BoundaryError(
                f"Grenz-ID '{grenz_id}': Fläche überschneidet sich zwischen "
                f"{a['name']}({a['x']}|{a['z']})-{b['name']}({b['x']}|{b['z']}) und "
                f"{c['name']}({c['x']}|{c['z']})-{d['name']}({d['x']}|{d['z']}) -- "
                f"Nummerierung im Spiel prüfen."
            )
        boundaries[grenz_id] = polygon
    return boundaries


def point_in_polygon(x, z, polygon):
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, z1 = polygon[i]
        x2, z2 = polygon[(i + 1) % n]
        if (z1 > z) != (z2 > z):
            x_int = x1 + (z - z1) * (x2 - x1) / (z2 - z1)
            if x < x_int:
                inside = not inside
    return inside


def _ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def segments_intersect(p1, p2, p3, p4):
    return _ccw(p1, p3, p4) != _ccw(p2, p3, p4) and _ccw(p1, p2, p3) != _ccw(p1, p2, p4)


def polygon_intersects_rect(polygon, minx, minz, maxx, maxz):
    corners = [(minx, minz), (maxx, minz), (maxx, maxz), (minx, maxz)]
    if any(minx <= px <= maxx and minz <= pz <= maxz for px, pz in polygon):
        return True
    if any(point_in_polygon(cx, cz, polygon) for cx, cz in corners):
        return True
    poly_edges = list(zip(polygon, polygon[1:] + polygon[:1]))
    rect_edges = list(zip(corners, corners[1:] + corners[:1]))
    return any(segments_intersect(pe[0], pe[1], re[0], re[1]) for pe in poly_edges for re in rect_edges)


def find_latest_export_dir(base_dir):
    if not base_dir.is_dir():
        raise FileNotFoundError(f"Export-Basisordner nicht gefunden: {base_dir}")
    candidates = [p for p in base_dir.iterdir() if p.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"Keine Export-Unterordner unter {base_dir} gefunden.")
    return max(candidates, key=lambda p: p.name)


def find_matching_tiles(export_dir, polygons):
    matches = []
    for f in export_dir.glob("*.png"):
        m = TILE_NAME_RE.match(f.name)
        if not m:
            continue
        x, z = int(m.group(1)), int(m.group(2))
        if any(polygon_intersects_rect(poly, x, z, x + TILE_SIZE, z + TILE_SIZE) for poly in polygons):
            matches.append(f)
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", required=True, help="Reich, z. B. montclair")
    args = parser.parse_args()

    scope = args.scope.lower()
    if scope not in REICH_COLORS:
        sys.exit(f"Unbekanntes Reich '{args.scope}'. Bekannt: {', '.join(sorted(REICH_COLORS))}")
    color = REICH_COLORS[scope]

    waypoints_file = Path(_require_env("WAYPOINTS_FILE"))
    export_base_dir = Path(_require_env("EXPORT_BASE_DIR"))

    if not waypoints_file.is_file():
        sys.exit(f"Wegpunkt-Datei nicht gefunden: {waypoints_file}")

    KARTEN_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(waypoints_file, WAYPOINTS_DEST)
    print(f"Wegpunkt-Datei nach {WAYPOINTS_DEST} kopiert (überschrieben, Versionierung über git).")

    waypoints = parse_waypoint_file(waypoints_file)
    border_points = [w for w in waypoints if w["set"] == BORDER_SET and w["color"] == color]
    if not border_points:
        sys.exit(f"Keine Grenz-Wegpunkte für '{scope}' im Set '{BORDER_SET}' (color {color}) gefunden.")

    try:
        boundaries = reconstruct_boundaries(border_points)
    except BoundaryError as e:
        sys.exit(f"Grenz-Wegpunkte für Reich '{scope}' prüfen: {e}")
    total_points = sum(len(p) for p in boundaries.values())
    print(
        f"{len(boundaries)} Grenzfläche(n) ({', '.join(sorted(boundaries))}) mit insgesamt "
        f"{total_points} Grenz-Wegpunkten rekonstruiert."
    )

    export_dir = find_latest_export_dir(export_base_dir)
    print(f"Verwende Export: {export_dir}")

    tiles = find_matching_tiles(export_dir, list(boundaries.values()))
    if not tiles:
        print("Warnung: keine Kacheln überschneiden die rekonstruierte Grenze.")

    scope_dir = KARTEN_DIR / scope
    if scope_dir.exists():
        shutil.rmtree(scope_dir)
    scope_dir.mkdir(parents=True)
    for t in tiles:
        shutil.copy2(t, scope_dir / t.name)

    print(f"{len(tiles)} Kachel(n) nach {scope_dir} kopiert (Ordner zuvor geleert, Versionierung über git).")


if __name__ == "__main__":
    main()
