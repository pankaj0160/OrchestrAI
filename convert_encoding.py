with open(r"c:\Generative AI\OrchestrAI\structure.txt", "r", encoding="utf-16le") as f:
    content = f.read()

with open(r"c:\Generative AI\OrchestrAI\structure_utf8.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("Converted successfully!")
