#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    import qiangheng

    qiangheng.main()


if __name__ == "__main__":
    profFileName = "profiles/prof.bin"

    import cProfile

    cProfile.run("main()", profFileName)

    try:
        import objgraph

        objgraph.show_most_common_types()
    except ImportError:
        pass

    import pstats

    p = pstats.Stats(profFileName)
    p.sort_stats("time").print_stats()
