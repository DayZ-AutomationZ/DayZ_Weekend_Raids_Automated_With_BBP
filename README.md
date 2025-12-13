# DayZ_Weekend_Raids_Automated_With_BBP
[![Day-Z-Automation-Z-(1).png](https://i.postimg.cc/cC0H7Jh0/Day-Z-Automation-Z-(1).png)](https://postimg.cc/PpVTTT0R)
### TL;DR

1. Copy `raid_mode.py` + both `cfggameplay_raid_*.json` + both `BBP_raid_*.json` to your Pi.
2. Make the two JSONs full copies of your real `cfggameplay.json` and `BBP_Settings.json` (only toggle the 2 booleans in each).
3. Add the contents of the real `cfggameplay.json` and `BBP_Settings.json` into both `cfggameplay_raid_*.json` + both `BBP_raid_*.json` (remember! only toggle the damage booleans in each). true / false and 1 or 0.
4. Put your FTP details into `raid_mode.py`.
5. Test once: `python3 raid_mode.py on` / `off`.
6. Add the cron block to `crontab -e`.

DayZ raid-mode switcher for Nitrado: a Raspberry Pi script that uploads raid-ON / raid-OFF cfggameplay.json via FTP. Automatically toggles disableBaseDamage and disableContainerDamage on a schedule (e.g. weekend raids) using cron. No extra DayZ mods required. Optional BaseBuildingPlus files. can be ignored. it will still work.

# Automatic Weekend Raids Mode (cfgGameplay switcher + optional BaseBuildingPlus switcher)

This package lets you toggle **raiding on/off** from a Raspberry Pi (or any machine with Python)
by uploading different config files to your DayZ server via FTP. 
NO NEED FOR MODS!! Simple ftp uploads via PI VPS or whatever you want to use running python Can even do it on your android!

It controls:
- `cfggameplay.json`  → vanilla bases / containers (disableBaseDamage, disableContainerDamage)
- `BBP_Settings.json` → BaseBuildingPlus structures (BBP_DisableDestroy)

You trigger it with:
```bash
python3 raid_mode.py on
python3 raid_mode.py off
```

and your cron schedule decides **when** raids are allowed.

---

## 1. Files in this package

Put all these files on your Pi in e.g. `/home/PIusername/dayz_raid`:

- `raid_mode.py`
- `cfggameplay_raid_on.json`
- `cfggameplay_raid_off.json`
- `BBP_raid_on.json`
- `BBP_raid_off.json`
- `README_RAID_MODE.md` (this file)
- `raid_scheduler.py` (set times here) you cannot use 01:05 for example.
- it simply is 1, 5 then best times to set are 17, 59 for example: when a server restarts 18:00
- upload files before restart at least a few minutes!, my server restarts 18:06, so 17:59 is a safe choice.
- dont forget to do `chmod +x /home/PIusername/dayz_raid/raid_scheduler.py` and `chmod +x /home/PIusername/dayz_raid/raid_mode.py`
- Set the times on line 17 in `raid_scheduler.py` Line 17: `if dow in (4, 5, 6) and time(17, 59) <= t < time(23, 59):` SO `time(17, 59)` is for Raid ON `time(23, 59)` is for Raid OFF

> If you don't use BaseBuildingPlus, you can ignore the BBP files.

---

## 2. Adjust the templates to your server

### 2.1 cfgGameplay templates

Open:

- `cfggameplay_raid_on.json`
- `cfggameplay_raid_off.json`

and **copy your own cfgGameplay.json** into both, then only change:

- In `cfggameplay_raid_on.json`:
  ```json
  "disableBaseDamage": false,
  "disableContainerDamage": false
  ```
- In `cfggameplay_raid_off.json`:
  ```json
  "disableBaseDamage": true,
  "disableContainerDamage": true
  ```

Keep all your other settings (stamina, UI, map, etc.) exactly the same as on your server.

### 2.2 BBP templates (optional, only if you use BBP)

Open:

- `BBP_raid_on.json`
- `BBP_raid_off.json`

and copy your own `BBP_Settings.json` content into both files.  
Then make sure:

- In `BBP_raid_on.json`:
  ```json
  "BBP_DisableDestroy": 0
  ```
  → BBP bases can be raided during the raid window.

- In `BBP_raid_off.json`:
  ```json
  "BBP_DisableDestroy": 1
  ```
  → BBP bases cannot be destroyed outside the raid window.

Keep all other BBP values (build anywhere, cement mixers, raid times, etc.) the same as you like.

---

## 3. Configure raid_mode.py ⚠️ Don’t share screenshots of this file, it contains your FTP password.

Edit `raid_mode.py` and set:

```python
FTP_HOST = "YOUR_FTP_HOST"
FTP_USER = "YOUR_FTP_USERNAME"
FTP_PASS = "YOUR_FTP_PASSWORD"
```

And adjust the remote paths if your host uses different folders:

```python
REMOTE_DIR_GAMEPLAY = "/dayzstandalone/mpmissions/dayzOffline.chernarusplus"
REMOTE_CFG_GAMEPLAY = "cfggameplay.json"

REMOTE_DIR_BBP = "/dayzstandalone/config/BaseBuildingPlus"
REMOTE_CFG_BBP = "BBP_Settings.json"
```

On Nitrado for Chernarus, this layout is correct:
- `cfggameplay.json` lives in `dayzstandalone/mpmissions/dayzOffline.chernarusplus`
- `BBP_Settings.json` lives in `dayzstandalone/config/BaseBuildingPlus`

---

## 4. Test manually

On the Pi, from the folder where `raid_mode.py` lives:

```bash
cd /home/PIusername/dayz_raid

# Switch raids OFF
python3 raid_mode.py off

# Then restart the DayZ server from the Nitrado panel
```

Join the server and check:
- You **cannot** damage vanilla fences/doors with tools.
- If you use BBP and BBP_raid_off.json was uploaded, BBP walls should also be indestructible.

Then test raids ON:

```bash
python3 raid_mode.py on
# restart server
```

Now:
- Vanilla fences/doors are raidable (depending on your cfgGameplay settings).
- BBP walls are raidable if `BBP_DisableDestroy` is 0 in the ON template.

---

## 5. Example cron schedule (Fri/Sat/Sun 18:00–00:00)

On the Pi, edit cron: (Change PIusername!) adjust times to your server restart times. make sure the files are uploaded at least a few minutes before restarts.

```bash
crontab -e
```

```cron

# --- RAID OFF / ON scheduler) ---
* * * * * /usr/bin/python3 /home/Piusername/dayz_raid/raid_scheduler.py >> /home/PIusername/dayz_raid/raid_scheduler.log 2>&1

```

- Times are server local time MAKE SURE THE PI or VPS or any machine you run this on has same server time setting as your server.
- Always restart the DayZ server **after** a config upload for it to take effect.

---

Have fun raiding only when **Your server** says it’s time. 🦌🔨 YOU NEED TO SET UP THE TIME in `raid_scheduler.py`
if your server starts around 18:00 set the time in `raid_scheduler.py` to 17:59 or even better 17:55.
The important thing is to set the time before server restarts occur. otherwise the switched files wont load to set raids on or off. 


## 6. Notes

- If you **don’t** use BBP:
  - Just ignore the BBP JSON files.
  - `raid_mode.py` will print a warning and move on if the BBP folder doesn’t exist.

- If Nitrado (or another host) UI overwrites cfgGameplay.json on restart:
  - Make sure you enable **Expert Mode** and **stop using the panel sliders** for base damage.
  - Your Pi + cron is now the boss for raid times.
