import sys
try:
    with open("generate_curriculum.py") as f:
        code = f.read()
    exec(code)
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()
