#include <stdlib.h>
#include <Python.h>
#include <string.h>

#ifdef __unix__
#define OS "unix"
#endif
#ifdef _WIN32
#define OS "windows"
#endif

char os[] = OS;

static PyObject *method_system(PyObject *self, PyObject *args) {
  char *command = NULL;
  int val = 0;
  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;
  val = system(command);
  return PyLong_FromLong(val);
}

static PyMethodDef system_mdef[] = {
  {"system", method_system, METH_VARARGS, "Python interface for C system function"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef system_module = {
  PyModuleDef_HEAD_INIT,
  "system",
  "Python interface for c system function",
  -1,
  system_mdef
};

PyMODINIT_FUNC PyInit_system(void) {
  PyObject *module = PyModule_Create(&system_module);
  PyModule_AddStringMacro(module, OS);
  return module;
}
