import subprocess
import difflib

LEX_PY = ["python3", "lex.py"]
LEX_C = ["./lex"]

def run_lexer(cmd, input_str):
    try:
        result = subprocess.run(
        cmd,
        input=input_str.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"ERROR: {e}"

def compare(input_str):
    out_py = run_lexer(LEX_PY, input_str)
    out_c = run_lexer(LEX_C, input_str)

    
    if out_py == out_c:
        return True, out_py, out_c

    diff = "\n".join(difflib.unified_diff(
        out_py.splitlines(),
        out_c.splitlines(),
        fromfile="lex.py",
        tofile="lexer.c",
        lineterm=""
    ))

    return False, out_py, out_c, diff
    

def test_cases():
    return [
        "/a\/b/",
        "/a",
        "a / b / c",
        "/a//b/",
        "/a/+b",
        "x = /abc/",
        "x = a / b",
        "/a/ /b/",
        "/a/ / b /",
        "/[a-z]+/",
        "/=/",
        "/ /",
        "/*/",
        "if (/a/.test(x))",
    ]

def fuzz_tests():
    base = ["a", "b", "/", "+", "-", "*", "=", "(", ")", " "]
    cases = []


    for a in base:
        for b in base:
            for c in base:
                cases.append(a + b + c)

    return cases


def main():
    print("=== TESTS MANUALES ===\n")


    for case in test_cases():
        ok, *res = compare(case)
        print(f"Input: {repr(case)}")

        if ok:
            print("OK\n")
        else:
            out_py, out_c, diff = res
            print("❌ DIFERENCIA")
            print("PY:\n", out_py)
            print("C:\n", out_c)
            print("diff:\n", diff)
            print("-" * 40)

    print("\n=== FUZZ TESTS ===\n")

    for case in fuzz_tests():
        ok, *res = compare(case)
        if not ok:
            out_py, out_c, diff = res
            print(f"❌ Caso encontrado: {repr(case)}")
            print("PY:\n", out_py)
            print("C:\n", out_c)
            print("diff:\n", diff)
            print("=" * 60)
            break
    else:
        print("No se encontraron diferencias en fuzz básico.")


if __name__ == "__main__":
    main()
