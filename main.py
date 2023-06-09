from argparse import ArgumentParser
from renderer import Renderer

def getArgs():
    parser = ArgumentParser(
        description="Creation De DonGeon",
        add_help=True
    )
    
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    
    parser.add_argument("--rooms", metavar="<ROOMS>", type=int, default=5)
    parser.add_argument("--seed",  metavar="<SEED>", type=int, default=None)
    
    parser.add_argument("--minwidth", metavar="<w>", type=int, default=4)
    parser.add_argument("--maxwidth", metavar="<W>", type=int, default=8)
    parser.add_argument("--minheight", metavar="<h>", type=int, default=4)
    parser.add_argument("--maxheight", metavar="<H>", type=int, default=8)
    
    parser.add_argument("--openings", metavar="<N>", type=int, default=2)
    parser.add_argument("--view-radius", metavar="<R>", type=int, default=6)
    parser.add_argument("--bonuses", metavar="<B>", type=int, default=2)
    parser.add_argument("--bonus-radius", metavar="<R>", type=int, default=3)
    parser.add_argument("--torch-delay", metavar="<D>", type=int, default=7)
    parser.add_argument("--hard", default=False, dest="hard", action="store_true")
    
    return parser.parse_args()


master = Renderer(getArgs())
master.mainloop()