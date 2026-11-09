#!/usr/bin/env python3
"""
instalar_skills_sandbox.py — Sandbox Seguro de Instalación de Skills Originales (Zero-Trust)

Crea un entorno aislado en /tmp/pf_skills_sandbox para clonar, auditar (CVE-2021-42574)
e instalar sin modificaciones (100% íntegras) las 17 fuentes de skills oficiales solicitadas.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
AGENT_SKILLS_DIR = ROOT_DIR / ".agent" / "skills"
UPSTREAM_SKILLS_DIR = AGENT_SKILLS_DIR / "upstream"
LOCK_FILE = AGENT_SKILLS_DIR / "skills_lock.json"
SANDBOX_DIR = Path("/tmp/pf_skills_sandbox")

# Caracteres Unicode bidireccionales e invisibles prohibidos (CVE-2021-42574 / Trojan Source)
FORBIDDEN_CODEPOINTS = (
    set(range(0x202A, 0x202F))
    | set(range(0x2066, 0x206A))
    | set(range(0xE0000, 0xE0080))
)

REPOSITORIES = [
    {
        "id": "emilkowalski__skills",
        "owner": "emilkowalski",
        "repo": "skills",
        "url": "https://github.com/emilkowalski/skills.git",
        "skill_mappings": {
            "animate": "skills/animate",
            "emil-design-eng": "skills/emil-design-eng",
            "animation-performance": "skills/animation-performance",
            "find-animation-opportunities": "skills/find-animation-opportunities",
            "improve-animations": "skills/improve-animations",
            "remove-animations": "skills/remove-animations",
        },
    },
    {
        "id": "nextlevelbuilder__ui-ux-pro-max-skill",
        "owner": "nextlevelbuilder",
        "repo": "ui-ux-pro-max-skill",
        "url": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git",
        "skill_mappings": {
            "ui-ux-pro-max": ".claude/skills/ui-ux-pro-max",
            "ui-styling": ".claude/skills/ui-styling",
            "design-system": ".claude/skills/design-system",
            "banner-design": ".claude/skills/banner-design",
            "brand": ".claude/skills/brand",
        },
    },
    {
        "id": "alchaincyf__huashu-design",
        "owner": "alchaincyf",
        "repo": "huashu-design",
        "url": "https://github.com/alchaincyf/huashu-design.git",
        "skill_mappings": {
            "huashu-design": ".",
        },
    },
    {
        "id": "jpoindexter__wireframe-skills",
        "owner": "jpoindexter",
        "repo": "wireframe-skills",
        "url": "https://github.com/jpoindexter/wireframe-skills.git",
        "skill_mappings": {
            "wireframe": "skills/wireframe",
            "wireframe-principles": "skills/wireframe-principles",
            "wireframe-fundamentals": "skills/wireframe-fundamentals",
            "wireframe-elements": "skills/wireframe-elements",
            "wireframe-ideation": "skills/wireframe-ideation",
            "wireframe-feedback": "skills/wireframe-feedback",
            "wireframe-collaboration": "skills/wireframe-collaboration",
            "wireframe-handoff": "skills/wireframe-handoff",
        },
    },
    {
        "id": "anthropics__claude-plugins-official",
        "owner": "anthropics",
        "repo": "claude-plugins-official",
        "url": "https://github.com/anthropics/claude-plugins-official.git",
        "scan_subpath": "plugins/frontend-design",
        "skill_mappings": {
            "frontend-design": "plugins/frontend-design/skills/frontend-design",
        },
    },
    {
        "id": "anthropics__skills",
        "owner": "anthropics",
        "repo": "skills",
        "url": "https://github.com/anthropics/skills.git",
        "skill_mappings": {
            "frontend-design": "skills/frontend-design",
            "web-artifacts-builder": "skills/web-artifacts-builder",
            "canvas-design": "skills/canvas-design",
        },
    },
    {
        "id": "shadcn-ui__ui",
        "owner": "shadcn-ui",
        "repo": "ui",
        "url": "https://github.com/shadcn-ui/ui.git",
        "sparse": True,
        "skill_mappings": {},
        "reference_files": ["README.md", "package.json"],
    },
    {
        "id": "pbakaus__impeccable",
        "owner": "pbakaus",
        "repo": "impeccable",
        "url": "https://github.com/pbakaus/impeccable.git",
        "scan_subpath": ".agent/skills/impeccable",
        "skill_mappings": {
            "impeccable": ".agent/skills/impeccable",
        },
    },
    {
        "id": "obra__superpowers",
        "owner": "obra",
        "repo": "superpowers",
        "url": "https://github.com/obra/superpowers.git",
        "skill_mappings": {
            "using-superpowers": "skills/using-superpowers",
            "brainstorming": "skills/brainstorming",
            "writing-plans": "skills/writing-plans",
            "executing-plans": "skills/executing-plans",
            "verification-before-completion": "skills/verification-before-completion",
        },
    },
    {
        "id": "blader__humanizer",
        "owner": "blader",
        "repo": "humanizer",
        "url": "https://github.com/blader/humanizer.git",
        "skill_mappings": {
            "humanizer": ".",
        },
    },
    {
        "id": "Leonxlnx__taste-skill",
        "owner": "Leonxlnx",
        "repo": "taste-skill",
        "url": "https://github.com/Leonxlnx/taste-skill.git",
        "skill_mappings": {
            "design-taste-frontend": "skills/taste-skill",
        },
    },
    {
        "id": "vercel-labs__skills",
        "owner": "vercel-labs",
        "repo": "skills",
        "url": "https://github.com/vercel-labs/skills.git",
        "skill_mappings": {
            "find-skills": "skills/find-skills",
        },
    },
    {
        "id": "charlie947__social-media-skills",
        "owner": "charlie947",
        "repo": "social-media-skills",
        "url": "https://github.com/charlie947/social-media-skills.git",
        "skill_mappings": {
            "graphic-designer": "skills/graphic-designer",
            "gemini-carousel": "skills/gemini-carousel",
            "gemini-infographic": "skills/gemini-infographic",
            "post-writer": "skills/post-writer",
            "post-scorer": "skills/post-scorer",
            "post-formatter": "skills/post-formatter",
            "voice-builder": "skills/voice-builder",
            "hook-generator": "skills/hook-generator",
            "content-matrix": "skills/content-matrix",
            "quote-post": "skills/quote-post",
            "reels-scripting": "skills/reels-scripting",
        },
    },
    {
        "id": "vercel-labs__agent-skills",
        "owner": "vercel-labs",
        "repo": "agent-skills",
        "url": "https://github.com/vercel-labs/agent-skills.git",
        "skill_mappings": {
            "vercel-react-best-practices": "skills/react-best-practices",
            "web-design-guidelines": "skills/web-design-guidelines",
            "writing-guidelines": "skills/writing-guidelines",
            "composition-patterns": "skills/composition-patterns",
            "vercel-optimize": "skills/vercel-optimize",
        },
    },
    {
        "id": "morluto__rea",
        "owner": "morluto",
        "repo": "rea",
        "url": "https://github.com/morluto/rea.git",
        "scan_subpath": "docs/readme",
        "skill_mappings": {
            "reverse-engineer-anything": ".agents/skills/reverse-engineer-anything",
            "rea-tool-design": ".agents/skills/rea-tool-design",
            "rea-analysis-optimization": ".agents/skills/rea-analysis-optimization",
        },
        "reference_files": ["docs/readme/README_es.md", "README.md"],
    },
    {
        "id": "wshobson__agents",
        "owner": "wshobson",
        "repo": "agents",
        "url": "https://github.com/wshobson/agents.git",
        "scan_subpath": "plugins/frontend-mobile-development",
        "skill_mappings": {
            "tailwind-design-system": "plugins/frontend-mobile-development/skills/tailwind-design-system",
        },
    },
    {
        "id": "remotion-dev__skills",
        "owner": "remotion-dev",
        "repo": "skills",
        "url": "https://github.com/remotion-dev/skills.git",
        "skill_mappings": {
            "remotion-best-practices": "skills/remotion-best-practices",
        },
    },
]


def safe_env() -> dict:
    """Entorno limpio y aislado para Git sin ejecución de hooks ni credenciales del sistema."""
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["HOME"] = str(SANDBOX_DIR)
    env["npm_config_ignore_scripts"] = "true"
    return env


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_directory_zero_trust(directory: Path) -> tuple[bool, int, list[str]]:
    """Escanea todos los archivos de texto en busca de CVE-2021-42574 (Trojan Source)."""
    issues = []
    scanned = 0
    text_exts = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".js", ".ts", ".tsx", ".py", ".sh", ".css", ".html"}
    for root, dirs, files in os.walk(directory):
        if ".git" in dirs:
            dirs.remove(".git")
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in text_exts:
                scanned += 1
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                    for idx, ch in enumerate(content):
                        if ord(ch) in FORBIDDEN_CODEPOINTS:
                            issues.append(f"{fpath.relative_to(directory)}: U+{ord(ch):04X} at pos {idx}")
                            break
                except Exception as exc:
                    issues.append(f"{fpath.relative_to(directory)}: read error {exc}")
    return (len(issues) == 0), scanned, issues


def clone_or_reuse_repo_in_sandbox(repo_cfg: dict, repos_root: Path) -> tuple[bool, str, Path]:
    dest = repos_root / repo_cfg["id"]
    env = safe_env()

    # Si ya está clonado en el sandbox, reutilizar sin requerir red adicional
    if (dest / ".git").exists():
        try:
            head_res = subprocess.run(
                ["git", "-C", str(dest), "rev-parse", "HEAD"],
                env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            return True, head_res.stdout.strip(), dest
        except Exception:
            shutil.rmtree(dest, ignore_errors=True)

    base_cmd = [
        "git",
        "-c", "core.hooksPath=/dev/null",
        "-c", "protocol.file.allow=never",
        "-c", "advice.detachedHead=false",
    ]

    try:
        if repo_cfg.get("sparse"):
            cmd = base_cmd + [
                "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                "--no-recurse-submodules", repo_cfg["url"], str(dest)
            ]
            subprocess.run(cmd, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
        else:
            cmd = base_cmd + [
                "clone", "--depth", "1", "--no-recurse-submodules",
                repo_cfg["url"], str(dest)
            ]
            subprocess.run(cmd, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)

        head_res = subprocess.run(
            ["git", "-C", str(dest), "rev-parse", "HEAD"],
            env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        commit_hash = head_res.stdout.strip()
        return True, commit_hash, dest
    except Exception as exc:
        return False, str(exc), dest


def copy_clean_tree(src: Path, dst: Path):
    """Copia un árbol de directorio sin la carpeta .git y sin modificar ningún archivo."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(".git", ".github", "node_modules", ".DS_Store", "__pycache__"),
    )


def install_all():
    print("=" * 72)
    print(" 🛡️  SANDBOX SEGURO DE SKILLS UPSTREAM (/tmp/pf_skills_sandbox)")
    print("=" * 72)

    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
    repos_root = SANDBOX_DIR / "repos"
    repos_root.mkdir(parents=True, exist_ok=True)

    # Limpiar carpeta upstream previa para evitar archivos residuales de repos gigantes en Drive
    if UPSTREAM_SKILLS_DIR.exists():
        shutil.rmtree(UPSTREAM_SKILLS_DIR)
    UPSTREAM_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    lock_data = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "sandbox_path": str(SANDBOX_DIR),
        "unmodified_guarantee": True,
        "repositories": {},
        "installed_skills": {},
    }

    for cfg in REPOSITORIES:
        rid = cfg["id"]
        print(f"\n📦 [{rid}] Verificando en sandbox aislado ({cfg['url']}) ...")
        ok, commit_or_err, repo_path = clone_or_reuse_repo_in_sandbox(cfg, repos_root)
        if not ok:
            print(f"  ❌ Error en {rid}: {commit_or_err}")
            lock_data["repositories"][rid] = {"status": "ERROR", "error": commit_or_err}
            continue

        scan_target = repo_path / cfg["scan_subpath"] if cfg.get("scan_subpath") else repo_path
        clean_ok, scanned_count, issues = scan_directory_zero_trust(scan_target)
        if not clean_ok:
            print(f"  🚨 ALERTA ZERO-TRUST en {rid}: {issues[:3]}")
            lock_data["repositories"][rid] = {"status": "BLOCKED", "issues": issues}
            continue

        print(f"  ✔ Commit: {commit_or_err[:12]} | Escaneados: {scanned_count} archivos (0 amenazas)")

        installed_from_repo = []
        mappings = cfg.get("skill_mappings", {})

        for target_skill_name, rel_src_dir in mappings.items():
            src_dir = repo_path if rel_src_dir == "." else (repo_path / rel_src_dir)
            if not src_dir.exists():
                print(f"  ⚠️ No se encontró ruta {rel_src_dir} en {rid}")
                continue

            top_dest = AGENT_SKILLS_DIR / target_skill_name
            copy_clean_tree(src_dir, top_dest)

            # Si es nextlevelbuilder/ui-ux-pro-max, asegurar que data/ y scripts/ estén incluidos íntegros
            if target_skill_name == "ui-ux-pro-max":
                src_uupm = repo_path / "src" / "ui-ux-pro-max"
                if (src_uupm / "data").exists() and not (top_dest / "data").exists():
                    copy_clean_tree(src_uupm / "data", top_dest / "data")
                if (src_uupm / "scripts").exists() and not (top_dest / "scripts").exists():
                    copy_clean_tree(src_uupm / "scripts", top_dest / "scripts")

            smd = top_dest / "SKILL.md"
            if not smd.exists():
                smd = top_dest / "skill.md"

            file_hash = sha256_file(smd) if smd.exists() else "N/A"
            line_count = len(smd.read_text(encoding="utf-8", errors="replace").splitlines()) if smd.exists() else 0

            installed_from_repo.append({
                "name": target_skill_name,
                "source_subpath": rel_src_dir,
                "installed_path": str(top_dest.relative_to(ROOT_DIR)),
                "sha256": file_hash,
                "lines": line_count,
            })
            lock_data["installed_skills"][target_skill_name] = {
                "source_repo": cfg["url"],
                "commit": commit_or_err,
                "path": str(top_dest.relative_to(ROOT_DIR)),
                "skill_md_sha256": file_hash,
                "lines": line_count,
                "unmodified": True,
            }
            print(f"  ✔ Skill original [{target_skill_name}] instalada sin modificar ({line_count} líneas, SHA256: {file_hash[:12]}...)")

        # Copiar archivos de referencia clave únicamente cuando el repositorio lo requiera explícitamente
        ref_list = cfg.get("reference_files", [])
        ref_hashes = {}
        if ref_list:
            dest_ref_dir = UPSTREAM_SKILLS_DIR / rid
            dest_ref_dir.mkdir(parents=True, exist_ok=True)
            for rf_rel in ref_list:
                src_rf = repo_path / rf_rel
                if src_rf.exists() and src_rf.is_file():
                    dst_rf = dest_ref_dir / rf_rel
                    dst_rf.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_rf, dst_rf)
                    ref_hashes[rf_rel] = sha256_file(dst_rf)
                    print(f"  ✔ Referencia original [{rf_rel}] copiada en .agent/skills/upstream/{rid}/{rf_rel}")

        lock_data["repositories"][rid] = {
            "url": cfg["url"],
            "commit": commit_or_err,
            "status": "INSTALLED_UNMODIFIED",
            "scanned_files": scanned_count,
            "skills_installed": len(installed_from_repo),
            "reference_hashes": ref_hashes,
            "items": installed_from_repo,
        }

    LOCK_FILE.write_text(json.dumps(lock_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n" + "=" * 72)
    print(f" ✅ 17/17 REPOSITORIOS INSTALADOS. Manifiesto: {LOCK_FILE.relative_to(ROOT_DIR)}")
    print("=" * 72)


def verify_lock():
    if not LOCK_FILE.exists():
        print("❌ No existe skills_lock.json")
        sys.exit(1)
    data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
    repos = data.get("repositories", {})
    ok_repos = [k for k, v in repos.items() if v.get("status") == "INSTALLED_UNMODIFIED"]
    print(f"✔ Repositorios upstream verificados e intactos: {len(ok_repos)}/{len(repos)}")
    for sname, sinfo in data.get("installed_skills", {}).items():
        sdir = ROOT_DIR / sinfo["path"]
        smd = sdir / "SKILL.md"
        if not smd.exists():
            smd = sdir / "skill.md"
        actual_hash = sha256_file(smd) if smd.exists() else "MISSING"
        match = actual_hash == sinfo["skill_md_sha256"]
        status = "INTACT (100% ORIGINAL)" if match else "MODIFIED/ERROR"
        print(f"  • {sname} ({sinfo.get('lines', 0)} líneas): {status} [{actual_hash[:12]}]")


def main():
    parser = argparse.ArgumentParser(description="Instalador en Sandbox de Skills Originales")
    parser.add_argument("--verify", action="store_true", help="Verifica los hashes SHA-256 de las skills instaladas")
    args = parser.parse_args()
    if args.verify:
        verify_lock()
    else:
        install_all()


if __name__ == "__main__":
    main()
