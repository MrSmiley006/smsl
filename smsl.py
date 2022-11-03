import sys, re, os

def resolve_includes(code, namespace=None):
    print(f"namespace: {namespace}")
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

            if namespace != None:
                regex = "namespace " + namespace + " \([\w\s=\"\[\],\(\)]+\)"
                code_list = code.split(re.search(regex, code))
                print(code_list)
                for i in code_list:
                    code = code.replace(i, "")
    ##print(code)
    return code

def add_defines(code, user_replaces):
    for i in code.split("\n"):
        i = i.split()
        #print(i)
        try:
            if i[0] == "#define":
                user_replaces[i[1]] = i[2]
                print(":D")
            elif i[0] == "#undef":
                del user_replaces[i[1]]
        except IndexError:
            pass

    return user_replaces


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
        code = re.sub(r"#include \"smsl.h\"", "", code)
        include_files = []
        for i in code_:
            i = i.split(" ")
            if i[0] == "#include" and i[1] != include_h.group().replace("#include ", ""):
                if re.match(r"![\w\.]*!", i[1]): i[1] = os.environ["SMSL_STDLIB"] + i[1]
                include_files.append(i[1].replace('"', "").replace("!", ""))

        for i in include_files:
            i_ = re.sub(r":\w+", "", i)
            try:
                include_file = open(i_)
            except FileNotFoundError:
                include_file = open(os.environ["SMSL_STDLIB"] + "/" + i_)
                
            resolved_file = resolve_includes(include_file.read(), re.sub("\w+.smsl:", "", i))
            print(f"i: {i.split(':')[1]}")
            include_file.close()
            if ":" in i:
                i = re.sub("\w+:", "", i)
                regex = "namespace " + i + " \([\w\s=\"\[\],\(\)]+\)"
                namespace = re.search(regex, resolved_file)
                if namespace != None:
                    print(f"{namespace}")
                    for i in resolved_file.split(namespace.group()):
                        resolved_file = resolved_file.replace(i, "")
            code = resolved_file + code
        ##print(code)

        code = code.split("\n")
        user_replaces = dict()
        for i in range(len(code)):
            if len(code[i]) > 0:
                #print(code[i].split()[0])
                if code[i].split()[0] in ["#define", "#undef"]:
                    user_replaces.update(add_defines(code[i], user_replaces))
                    #print(f"user_replaces: {str(user_replaces)}")
            for j in user_replaces:
                j_ = j.replace("+", " ").replace("\\n", "\n").replace("\ ", "+")
                if not code[i].startswith("#"):
                    code[i] = code[i].replace(user_replaces[j], j_)
        code = "\n".join(code)
        print(code)
        
        ##print(code)
        for i in replaces:
            j = replaces[i].replace("+", " ").replace("\\n", "\n")
            i = i.replace("+", " ").replace("\\n", "\n")
            
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
#           "func"        : "def",
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
