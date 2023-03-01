from distutils.core import setup, Extension

def main():
    setup(name="system",
          version="1.0.0",
          description="Python interface for the system C library function",
          author="<your name>",
          author_email="your_email@gmail.com",
          ext_modules=[Extension("system", ["system.c"])])

if __name__ == "__main__":
    main()
