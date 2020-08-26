import math
import sys
import numpy as np
from svgpathtools import svg2paths, wsvg, parse_path, CubicBezier, Arc, QuadraticBezier, Line
import level
import msgport
from xml.dom import minidom

try:
    from tkinter import filedialog, Tk
except ImportError:
    from Tkinter import Tk
    import tkFileDialog as filedialog


try:
    i_input = raw_input
except:
    i_input = input
def mad(data, axis=None):
    return np.mean(abs(data - np.mean(data, axis)), axis)


def slope(x1, y1, x2, y2):
    try:
        m = math.atan2(y2 - y1, x2 - x1)
    except Exception:
        return 0
    else:
        return m


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print(sys.argv)
        root = Tk()
        root.withdraw()
        root.update()
        file_path = filedialog.askopenfilename(
            filetypes=[('Vector file', '*.svg')]
            )
        root.update()
        del root
    scale = float(input("size of level (higher number means smaller size):"))
    density = float(input("block density (default 1):"))
    scale/=density
    block_size = float(input("block size (default 0.3):"))

    # new data~
    """mydoc = minidom.parse(file_path)
    path_tag = mydoc.getElementsByTagName("path")
    d_string = path_tag[0].attributes['d'].value"""
    #end new data
    pths, _ = svg2paths(file_path)
    wsvg(pths, filename='.tmp.svg')
    paths, _ = svg2paths('.tmp.svg')
    pathsxy = []
    lvl = level.Level("ggd")
    for path in paths:
        x_paths = [0.1]
        y_paths = [0.1]
        slopes = []
        for p in path:
            p.start /= scale
            p.end /= scale
            if isinstance(p, CubicBezier):
                p.control1 /= scale
                p.control2 /= scale
            elif isinstance(p, Arc):
                p.radius /= scale
            elif isinstance(p, QuadraticBezier):
                p.control /= scale
            elif not isinstance(p, Line):

                print(p)
            for i in range(int(round(p.length()))):
                comp = p.point(i / p.length())
                slopes.append(slope(x_paths[-1], y_paths[-1], comp.real, comp.imag))
                x_paths.append(comp.real)
                y_paths.append(comp.imag)
        pathsxy.append(np.column_stack((x_paths[1:], y_paths[1:], slopes, )))
    svglengthy = max(np.concatenate([l[:, 1] for l in pathsxy]))
    total = 0
    for path in pathsxy:
        for point in path:
            total += 1
            lvl.addBlock(917, (point[0]*2)/density, (((-1*point[1])+svglengthy)*2)/density,
                         rotation=math.degrees(point[2]), size=block_size,
                         dont_fade=1, dont_enter=1)
    print("Objects used: "+str(total) +
          ". Note: if the level uses over 3000 objects, it might not load")
    msgport.uploadToGD(lvl)
    #lid = lvl.uploadLevel(uname, password, lpassword="1", description="")
    #print('Your level ID is '+str(lid))
    i_input("Pasted the level. Press enter to exit")


if __name__ == '__main__':
    main()
