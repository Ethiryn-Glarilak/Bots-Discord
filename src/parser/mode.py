from src.parser.parser.parser import Parser
from src.parser.lexer.lexer_default import word_token

class Mode:
    def __getattribute__(self, __name : str):
        if "MODE_" in __name:
            return self.parser(__name)
        return super().__getattribute__(__name)

    def __call__(self, prefix):
        self.prefix = prefix
        return self

    def pop_prefix(self):
        prefix = getattr(self, "prefix", None)
        if prefix is None:
            return "0"
        delattr(self, "prefix")
        return prefix

    def parser(self, __name : str):
        prefix = self.pop_prefix()
        parser = Parser(prefix)
        for add in super().__getattribute__(__name):
            add = add(prefix)
            parser.rules.update(add[1])
            parser.rules.get("default").extend(add[2])
            parser.lexer.mode.get("spc_token_").update(add[0].get("spc_token_", {}))
            parser.lexer.mode.get("esc_token_").update(add[0].get("esc_token_", {}))
            parser.lexer.mode["spc_char__"] = parser.lexer.mode.get("spc_char__") + add[0].get("spc_char__", "")

            word_token(parser.lexer, add[0].get("word_token", []))

        return parser
