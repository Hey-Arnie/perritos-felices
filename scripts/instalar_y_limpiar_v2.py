#!/usr/bin/env python3
"""
instalar_y_limpiar_v2.py — Vendoring Seguro de Agent Skills & Zero-Trust Sandbox
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
WEB_DIR = SCRIPTS_DIR.parent
ROOT_DIR = WEB_DIR.parent
SANDBOX_DIR = Path("/tmp/pf_vendor_sandbox")
LOCK_FILE = ROOT_DIR / "vendor_lock.json"

HUB_MAPPING = {
    "pf-design-guardian": {
        "taste-skill": "https://github.com/Leonxlnx/taste-skill.git",
        "impeccable": "https://github.com/pbakaus/impeccable.git",
    },
    "pf-editorial-cms": {
        "humanizer": "https://github.com/blader/humanizer.git",
        "marketingskills": "https://github.com/coreyhaines31/marketingskills.git",
    },
    "pf-social-factory": {
        "huashu-design": "https://github.com/alchaincyf/huashu-design.git",
        "social-media-skills": "https://github.com/social-media-skills/skills.git",
        "character-design-sheet": "https://github.com/Saeyeon-developer/character-design-sheet.git",
    },
    "pf-video-director": {
        "hyperframes": "https://github.com/heygen-com/hyperframes.git",
        "emilkowalski-skills": "https://github.com/emilkowalski/skills.git",
    },
    "pf-security-zerotrust": {
        "trailofbits-skills": "https://github.com/trailofbits/skills.git",
        "getsentry-skills": "https://github.com/getsentry/skills.git",
    },
}

DELETION_TARGETS = [
    ROOT_DIR / "05_Studio_Privado" / "blender_assets",
    ROOT_DIR / "05_Studio_Privado" / "buck_felicidad_perros" / "blender_assets",
    ROOT_DIR / "05_Studio_Privado" / "buck_felicidad_perros" / "blender_frames",
    ROOT_DIR / "05_Studio_Privado" / "buck_felicidad_perros" / "stills_blender_rig",
    ROOT_DIR / "05_Studio_Privado" / "buck_felicidad_perros" / "blender_rig_and_render.py",
    ROOT_DIR / "05_Studio_Privado" / "buck_felicidad_perros" / "felicidad_perros_rigged.blend",
    ROOT_DIR / "05_Studio_Privado" / "motion_studio" / "node_modules",
    ROOT_DIR / "05_Studio_Privado" / "motion_studio" / ".venv",
    ROOT_DIR / ".agents" / "teamwork",
    ROOT_DIR / "vercel.json",
    WEB_DIR / "vercel.json",
]


def compute_dir_hash(directory: Path) -> str:
    hasher = hashlib.sha256()
    for p in sorted(directory.rglob("*")):
        if p.is_file() and not p.name.startswith(".git"):
            hasher.update(p.relative_to(directory).as_posix().encode())
            hasher.update(p.read_bytes())
    return hasher.hexdigest()


def setup_vendor() -> None:
    print("[*] Iniciando proceso Zero-Trust Skill Vendoring...")
    if SANDBOX_DIR.exists():
        shutil.rmtree(SANDBOX_DIR)
    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
    lock_data = {}

    for hub_name, repos in HUB_MAPPING.items():
        hub_upstream = ROOT_DIR / ".agent" / "skills" / hub_name / "upstream"
        hub_upstream.mkdir(parents=True, exist_ok=True)
        for skill_id, url in repos.items():
            sandbox_target = SANDBOX_DIR / skill_id
            print(f"  [+] Clonando {skill_id}...")
            env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
            subprocess.run(
                [
                    "git",
                    "-c", "filter.lfs.smudge=",
                    "-c", "filter.lfs.required=false",
                    "-c", "filter.lfs.process=",
                    "clone", "--depth", "1", url, str(sandbox_target),
                ],
                check=True,
                env=env,
            )
            final_target = hub_upstream / skill_id
            if final_target.exists():
                shutil.rmtree(final_target)
            shutil.copytree(
                sandbox_target, final_target, ignore=shutil.ignore_patterns(".git*")
            )
            lock_data[f"{hub_name}/{skill_id}"] = {
                "url": url,
                "sha256": compute_dir_hash(final_target),
            }

    # Include any existing local upstream skills in lock_data
    for hub_dir in sorted((ROOT_DIR / ".agent" / "skills").iterdir()):
        up = hub_dir / "upstream"
        if not up.is_dir():
            continue
        for item in sorted(up.iterdir()):
            key = f"{hub_dir.name}/{item.name}"
            if item.is_dir() and key not in lock_data:
                lock_data[key] = {"sha256": compute_dir_hash(item)}

    LOCK_FILE.write_text(json.dumps(lock_data, indent=2) + "\n", encoding="utf-8")
    print(f"[*] Vendor lock actualizado en {LOCK_FILE.name} ({len(lock_data)} skills).")


def verify_vendor() -> int:
    if not LOCK_FILE.exists():
        print("ERROR: vendor_lock.json no encontrado.")
        return 1
    lock_data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
    failures = 0
    for key, meta in sorted(lock_data.items()):
        hub, skill = key.split("/", 1)
        target = ROOT_DIR / ".agent" / "skills" / hub / "upstream" / skill
        if not target.exists():
            print(f"[FALTA] {key}")
            failures += 1
            continue
        if compute_dir_hash(target) != meta["sha256"]:
            print(f"[HASH_MISMATCH] {key}")
            failures += 1
    print(f"Verificación vendor_lock.json: {len(lock_data) - failures}/{len(lock_data)} OK.")
    return 1 if failures else 0


def clean_targets() -> None:
    for target in DELETION_TARGETS:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            print(f"  [X] Eliminado: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Vendoring y limpieza Zero-Trust PF-2027")
    parser.add_argument("--install", action="store_true", help="Clonar repos upstream y regenerar vendor_lock.json")
    parser.add_argument("--clean", action="store_true", help="Purgar artefactos obsoletos")
    parser.add_argument("--verify", action="store_true", help="Verificar hashes en vendor_lock.json")
    args = parser.parse_args()

    if args.install:
        setup_vendor()
    if args.clean or args.install:
        clean_targets()
    rc = verify_vendor() if (args.verify or not args.install) else 0
    audit = subprocess.run([sys.executable, str(SCRIPTS_DIR / "publicar.py"), "audit"])
    return rc or audit.returncode


if __name__ == "__main__":
    raise SystemExit(main())
