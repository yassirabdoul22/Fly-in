from typing import List, Dict, Optional


class Token:
    def __init__(
        self,
        type_: str,
        value: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        line_number: Optional[int] = None,
        line_content: Optional[str] = None
    ):
        self.type = type_             
        self.value = value           
        self.x = x
        self.y = y
        self.metadata = metadata or {}
        self.line_number = line_number
        self.line_content = line_content

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value}, x={self.x}, y={self.y}, metadata={self.metadata})"



class Lexer:
    def __init__(self, filename: str):
        self.filename = filename
        self.lines: List[str] = []    
        self.tokens: List[Token] = [] 
        self.current_line_number: int = 0

    def read_file(self):
        try:
            with open(self.filename, "r") as f:
                for raw_line in f:
                    self.current_line_number += 1
                    line = raw_line.strip()
                    # ignorer lignes vides et commentaires
                    if not line or line.startswith("#"):
                        continue
                    self.lines.append(line)
        except FileNotFoundError:
            print(f"Error: file '{self.filename}' not found.")
            raise

    def tokenize_line(self, line: str, line_number: int) -> Token:
        if line.startswith("nb_drones"):
            value = int(line.split(":")[1].strip())
            return Token(type_="nb_drones", value=value, line_number=line_number, line_content=line)

        elif line.startswith("start_hub") or line.startswith("end_hub") or line.startswith("hub"):
            parts = line.split()
            type_ = parts[0][:-1]
            name = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            metadata = {}
            if "[" in line and "]" in line:
                meta_str = line[line.find("[")+1:line.find("]")]
                for item in meta_str.split():
                    if "=" in item:
                        key, val = item.split("=")
                        metadata[key] = val
            return Token(type_=type_, value=name, x=x, y=y, metadata=metadata, line_number=line_number, line_content=line)

        elif line.startswith("connection"):
            parts = line.split(":")[1].strip().split()[0]  # "A-B"
            zone1, zone2 = parts.split("-")
            metadata = {}
            if "[" in line and "]" in line:
                meta_str = line[line.find("[")+1:line.find("]")]
                for item in meta_str.split():
                    if "=" in item:
                        key, val = item.split("=")
                        metadata[key] = val
            return Token(type_="connection", value=(zone1, zone2), metadata=metadata, line_number=line_number, line_content=line)

        else:
            raise ValueError(f"Unknown line type at line {line_number}: {line}")

    def tokenize(self) -> List[Token]:
        self.tokens = []
        for i, line in enumerate(self.lines):
            token = self.tokenize_line(line, i+1)
            self.tokens.append(token)
        return self.tokens
