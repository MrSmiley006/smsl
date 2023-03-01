#include <windows.h>
#include <Python.h>

static PyObject *method_beep(PyObject *self, PyObject *args) {
  int *freq, *time = NULL;
  if (!PyArg_ParseTuple(args, "dd", &freq, &time))
    return NULL;
  Beep(freq, time);
  return PyLong_FromLong(0);
}

static PyMethodDef beep_mdef[] = {
  {"beep", method_beep, METH_VARARGS, "Python interface for C Beep function (Windows-only)"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef beep_module = {
  PyModuleDef_HEAD_INIT,
  "system",
  "Python interface for C Beep function (windows-only)",
  -1,
  beep_mdef
};

PyMODINIT_FUNC PyInit_system(void) {
  return PyModule_Create(&system_module);
}

