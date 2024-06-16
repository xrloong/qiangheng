#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    import qiangheng

    qiangheng.main()


if __name__ == "__main__":
    profFileName = "profiles/prof.bin"

    import profile

    profile.run("main()", profFileName)

    import objgraph

    objgraph.show_most_common_types()

    import pstats

    p = pstats.Stats(profFileName)
    p.sort_stats("time").print_stats()
