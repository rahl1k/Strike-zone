import re
from pathlib import Path

p = Path('server.js')
s = p.read_text(encoding='utf-8')

if '"butterfly"' in s and 'player.state.weapon === "butterfly"' in s:
    print('Server Butterfly support already present')
    raise SystemExit(0)

s, n1 = re.subn(
    r'\[\s*"rifle"\s*,\s*"pistol"\s*,\s*"knife"\s*\]\s*\.includes\(\s*data\.weapon\s*\)',
    '["rifle", "pistol", "knife", "butterfly"].includes(data.weapon)',
    s,
    count=1,
)

s, n2 = re.subn(
    r'weapon\s*===\s*"knife"',
    '(weapon === "knife" || weapon === "butterfly")',
    s,
    count=2,
)

s, n3 = re.subn(
    r'player\.state\.weapon\s*===\s*"knife"',
    '(player.state.weapon === "knife" || player.state.weapon === "butterfly")',
    s,
    count=1,
)

if n1 != 1 or n2 != 2 or n3 != 1:
    raise RuntimeError(f'Unexpected server patch counts: validation={n1}, knifeChecks={n2}, damage={n3}')

p.write_text(s, encoding='utf-8')
print('Butterfly server support installed')
