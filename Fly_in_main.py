from src.parser.lexer import Lexer
from src.parser.parser import Parser
import os


def main():
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "map.txt"
    )

    # ---------- LEXER ----------
    lexer = Lexer(config_path)
    lexer.read_file()
    tokens = lexer.tokenize()

    print("TOKENS:")
    for t in tokens:
        print(t)

    print("\n----------------------\n")

    # ---------- PARSER ----------
    parser = Parser(tokens)
    config = parser.parse()

    print("NB DRONES:", config.nb_drones)
    print("START:", config.start_zone.name)
    print("GOAL:", config.goal_zone.name)

    print("\nZONES:")
    for z in config.graph.zones.values():
        print(z.name, z.z_type)

    print("\nCONNECTIONS:")
    for k, v in config.graph.connections.items():
        print(k, "->", v)


if __name__ == "__main__":
    main()
