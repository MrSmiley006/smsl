import sys, re, os

def resolve_includes(code):
    code_ = code.split("\n")
    include_type = ""
    for i in code_:
        include = re.match(r"#include \"[\w\.!]*\"", i)
        if include != None and not '#include "smsl.h"' in i:
            include_file = include.group().replace("#include ", "").replace('"', "")
            if "!" in include_file:
                include_file = os.environ["SMSL_STDLIB"] + include_file.replace("!", "")
            with open(include_file) as f:
                code = re.sub(include.group(), f.read(), code)
                include = re.match(r"#include \"[\w.]*\"", i)
    ##print(code)
    return code


def run(stage, code=None):
    if stage == 1:
        include_h = re.search(r'#include "\w*\.h"', code)
        replaces = dict()
        """
        Sestaví slovník ze souboru definic uvedeného v SmSL programu.
        Ten se následně použije k nahrazení závorek a klíčových slov.
        """
        if include_h:
            #print(include_h)
            with open(include_h.group().replace("#include ", "").replace('"', "")) as def_file:
                define = def_file.readlines()
                for i in define:
                    #print(i)
                    type(i)
                    if i.startswith("#define "):
                        i = i.replace("#define ", "").replace("\n", "")
                    else:
                        continue

                    for j in ["var", "new"]:
                        i = i.replace(j, "")
                    i = i.split(" ")
                    if len(i) == 1: i.append("")
                    try: replaces[i[0]]
                    except KeyError: replaces[i[0]] = i[1]
                #print(replaces)

        code_ = code.split("\n")
        """
        Přidá do SmSL souboru obsah všech souborů v něm uvedených (vyjma .h souborů)
        """
        code = re.sub(r"#include smsl.h", "", code)
        include_files = []
        for i in code_:
            i = i.split(" ")
            if i[0] == "#include" and i[1] != include_h.group().replace("#include ", ""):
                if re.match(r"![\w\.]*!", i[1]): i[1] = os.environ["SMSL_STDLIB"] + i[1]
                include_files.append(i[1].replace('"', "").replace("!", ""))

        for i in include_files:
            include_file = open(i)
            resolved_file = resolve_includes(include_file.read())
            code = resolved_file + code
        ##print(code)

        ##print(code)
        for i in replaces:
            j = replaces[i].replace("+", " ")
            i = i.replace("+", " ")
            if not "-d" in sys.argv and not "--decompile" in sys.argv:
                code = code.replace(j, i)
            else:
                code = code.replace(i, j)
        
        """indent_count = 0
        indented_code = []
        indent = ""
        code_ = code.split("\n")
        for i in code_:
            i_ = i
            if "(" in i:
                    indent_count += 1
                    indent = "\t" * indent_count
            elif ")" in i:
                    indent_count -= 1
                    indent = "\t" * indent_count
            #if not i == i_:
            i = indent + i
            indented_code.append(i)

        code = "\n".join(indented_code)"""
        if "-m" in sys.argv:
            with open("pyfile.py", "w") as f:
                f.write(code)
                sys.exit()

        #print(code)


        py_replaces = {
            "CALL_START"  : "(",
            "CALL_END"    : ")",
            "BLOCK_START" : ":",
            "BLOCK_END"   : "#BLOCK_END",
            "LIST_START"  : "[",
            "LIST_END"    : "]",
            "DICT_START"  : "{",
            "DICT_END"    : "}",
            "LAMBDA"      : "lambda",
            "func"        : "def",
            "write"       : "print",
            "WRITE"       : "write",
            "var "        : "",
            "new"         : "",
            "catch"       : "except",
            "else if"     : "elif",
            "true"        : "True",
            "false"       : "False"
        }

        for i in py_replaces:
            code = code.replace(i, py_replaces[i])

        if "-p" in sys.argv:
            with open("pyfile.py", "w") as f:
                f.write(code)

        return code

    if stage == 2:
        code = compile(code, "pyfile.py", "exec")
        exec(code, globals(), globals())


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        run(2, run(1, f.read()))
