class Instruction:
    Op: str
    Src: str | int
    Dest: str
    LineIndex: int
    Label: str

    def __init__(self, op, line_index, src="", dest="", label="") -> None:
        self.Op = op
        self.Src = src
        self.Dest = dest
        self.LineIndex = line_index
        self.Label = label

    def __repr__(self) -> str:
        return f"\n[\t{self.Op} \t{self.Src}\t {self.Dest}\tIndex={self.LineIndex}]"

    def __str__(self) -> str:
        if self.Label != "":
            return f"{self.Op} {self.Src} {self.Dest}\tIndex={self.LineIndex}\tLabel={self.Label}"
        else:
            return f"{self.Op} {self.Src} {self.Dest}\tIndex={self.LineIndex}"