with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
depth = 0
for i, line in enumerate(lines):
    line_stripped = line.strip()
    if line_stripped.startswith('//'):
        continue
    o = line.count('{')
    c = line.count('}')
    depth += o
    depth -= c
    if depth < 0 or (depth == 0 and c > 0) or o > 0 or c > 0:
        out.append(f"{i+1}: D={depth} | {line.strip()}")

with open('brace_depth.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out))
