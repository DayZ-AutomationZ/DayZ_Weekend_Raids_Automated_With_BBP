import ftplib
import sys
from pathlib import Path

# === FTP SETTINGS ===
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"

# === REMOTE PATHS (ADJUST FOR YOUR HOST) ===
# Example for Nitrado:
#   cfgGameplay.json  -> /dayzstandalone/mpmissions/dayzOffline.chernarusplus
#   BBP_Settings.json -> /dayzstandalone/config/BaseBuildingPlus
REMOTE_DIR_GAMEPLAY = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus"
REMOTE_CFG_GAMEPLAY = "cfggameplay.json"

REMOTE_DIR_BBP = "/dayzstandalone/config/BaseBuildingPlus"
REMOTE_CFG_BBP = "BBP_Settings.json"

# === LOCAL PATHS ON YOUR PI ===
LOCAL_DIR = Path("/home/PIusername/dayz_raid")  # adjust if needed

def upload_file(ftp: ftplib.FTP, local_file: Path, remote_dir: str, remote_name: str, label: str):
    if not local_file.exists():
        print(f"[WARN] {label}: Local file does not exist, skipping: {local_file}")
        return

    print(f"[{label}] Changing to remote dir: {remote_dir}")
    ftp.cwd(remote_dir)

    with open(local_file, "rb") as f:
        print(f"[{label}] Uploading {local_file.name} -> {remote_name}")
        ftp.storbinary(f"STOR {remote_name}", f)

    print(f"[{label}] Upload complete.")

def upload_mode(mode: str):
    mode = mode.lower()
    if mode not in ("on", "off"):
        raise SystemExit("Mode must be 'on' or 'off'")

    # Pick the right templates
    local_cfg_gameplay = LOCAL_DIR / f"cfggameplay_raid_{mode}.json"
    local_cfg_bbp = LOCAL_DIR / f"BBP_raid_{mode}.json"

    print(f"[RAID {mode.upper()}] Connecting to FTP {FTP_HOST} ...")
    with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        ftp.login()
        print("[FTP] Login OK.")

        # Upload cfgGameplay.json (vanilla/base damage)
        upload_file(
            ftp,
            local_cfg_gameplay,
            REMOTE_DIR_GAMEPLAY,
            REMOTE_CFG_GAMEPLAY,
            "cfgGameplay"
        )

        # Try upload BBP settings (optional)
        try:
            upload_file(
                ftp,
                local_cfg_bbp,
                REMOTE_DIR_BBP,
                REMOTE_CFG_BBP,
                "BBP_Settings"
            )
        except ftplib.error_perm as e:
            print(f"[BBP_Settings] FTP error (maybe BBP folder not present?): {e}")
        except Exception as e:
            print(f"[BBP_Settings] Unexpected error: {e}")

    print(f"[RAID {mode.upper()}] All done.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 raid_mode.py on|off")
        raise SystemExit(1)
    upload_mode(sys.argv[1])
