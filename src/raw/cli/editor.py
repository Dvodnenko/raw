import tempfile
import subprocess
import os


def from_editor(title: str, initial_text: str = ""):
    with tempfile.NamedTemporaryFile(
        mode="w",prefix=title+"_", suffix=".txt",
        delete_on_close=False, delete=False
    ) as tmpfile:
        tmpfile.write(initial_text)

    subprocess.run(["open", "-a", "TextEdit", "-W", tmpfile.name])
    with open(tmpfile.name, "r") as file:
        content = file.read()
        
    os.remove(tmpfile.name)

    return content
