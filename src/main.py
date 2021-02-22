from graphviz import Digraph
import util
import os
from pathlib import Path
import datamap
import leetcode

def get_map(map_file):
    path = Path(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(path.parent.parent, "map", map_file))


def get_leetcode_txt(file):
    f = open(get_map(file), "r", encoding="utf-8")
    t = f.read()
    return t

def generate_leetcode(leet, file, slug, out_name):
    m = datamap.DataMap(get_leetcode_txt(file))
    g = Digraph('stones', encoding='utf-8')

    for n in m.nodes:
        if not n.is_root:
            g.node(name=n.name, style='filled', fillcolor="lightslategray", color='lightgrey', fontcolor="white", fontname="Microsoft YaHei", shape='box')
            g.edge(n.parent, n.name)
        else:
            g.node(name=n.name, style='filled', target="_parent", href="https://leetcode-cn.com/tag/"+slug, fillcolor="orangered", color='lightgrey', fontcolor="white", fontname="Microsoft YaHei", shape='box')

        # add problem
        last = ""
        for p in n.problems:
            title = leet.get_title(p)
            level = leet.get_level(p)
            problem = leet.get_problem(p)
            idstr = str(p)
            title = idstr+". "+title
            color = "lightgrey"

            if level == "Easy":
                color = "greenyellow"
            elif level == "Medium":
                color = "orange"
            elif level == "Hard":
                color = "red"
            else:
                print("unknown level:", level)
            slug = problem['data']['question']['questionTitleSlug']
            g.node(name=idstr, label=title, target="_parent", href="https://leetcode-cn.com/problems/"+slug, color=color, fontname="Microsoft YaHei", shape='box')
            if len(last) > 0:
                g.edge(last, idstr)
            else:
                g.edge(n.name, idstr)
            last = idstr

    g.format = 'svg'
    g.render(filename=util.get_images(out_name))
    os.remove(util.get_images(out_name))

def main():
    leet = leetcode.Leetcode()
    leet.update_db()
    generate_leetcode(leet, "leetcode-dp.txt", "dynamic-programming", "leetcode_dp")
    generate_leetcode(leet, "leetcode-tree.txt", "tree", "leetcode_tree")
    leet.close_db()

if __name__ == "__main__":
    main()
