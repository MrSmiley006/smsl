#include <stdlib.h>
#include <time.h>
#include <Python.h>

static PyObject *method_rand_gen(PyObject *self, PyObject *args) {
  // int *num = NULL;
  //if (!(PyArg_ParseTuple(args, "i",  &num))) return NULL;
  int _num = rand();
  return PyLong_FromLong(_num);
}

static PyMethodDef RandMethods[] = {
  {"rand_gen", method_rand_gen, METH_VARARGS, "Generátor náhodných čísel"},
  {NULL, NULL, 0, NULL}
};

static PyModuleDef randmodule = {
  PyModuleDef_HEAD_INIT,
  "rand_gen",
  "Generátor náhodných čísel",
  -1,
  RandMethods
};

PyMODINIT_FUNC PyInit_rand_gen(void) {
  srand(time(0));
  return PyModule_Create(&randmodule);
}
