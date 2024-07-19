class Instruction:

    def __init__(self, op, line_index, src="", dest="", label="") -> None:
        self.Op: str = op
        self.Src: str | int = src
        self.Dest: str = dest
        self.LineIndex: str = line_index
        self.Label: str = label

    def __repr__(self) -> str:
        return f"\n[\t{self.Op} \t{self.Src}\t {self.Dest}\tIndex={self.LineIndex}]"

    def __str__(self) -> str:
        if self.Label != "":
            return f"{self.Op} {self.Src} {self.Dest}\tIndex={self.LineIndex}\tLabel={self.Label}"
        else:
            return f"{self.Op} {self.Src} {self.Dest}\tIndex={self.LineIndex}"
