from argparse import ArgumentParser
from renderer import GridRenderer
from generation import DungeonGenerator

def getArgs():
    parser = ArgumentParser(
        description="Creation De DonGeon",
        add_help=True
    )
    
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    
    parser.add_argument("--rooms", metavar="<ROOMS>", type=int, required=False, default=5)
    parser.add_argument("--seed",  metavar="<SEED>", type=int, default=None)
    
    parser.add_argument("--minwidth", metavar="<w>", type=int, default=4)
    parser.add_argument("--maxwidth", metavar="<W>", type=int, default=8)
    parser.add_argument("--minheight", metavar="<h>", type=int, default=4)
    parser.add_argument("--maxheight", metavar="<H>", type=int, default=8)
    
    parser.add_argument("--openings", metavar="<N>", type=int, default=2)
    parser.add_argument("--hard", default=False, dest="hard", action="store_true")
    
    return parser.parse_args()

master = DungeonGenerator(getArgs())
renderer = GridRenderer(master.generate()['grid']).show()