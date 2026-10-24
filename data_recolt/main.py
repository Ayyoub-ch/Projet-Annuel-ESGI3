from pathlib import Path
import subprocess
import sys


def main():
    dossier_scripts = Path(__file__).resolve().parent
    dossier_projet = dossier_scripts.parent
    scripts = (
        "league.py",
        "matchs.py",
        "serie.py",
        "tournament.py",
    )

    for nom_script in scripts:
        script = dossier_scripts / nom_script
        subprocess.run(
            [sys.executable, str(script)],
            cwd=dossier_projet,
            check=True,
        )


if __name__ == "__main__":
    main()