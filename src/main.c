#include <Python.h>
#include <stdio.h>
#include "../libcsv.h"

static PyObject *pModule;
static PyObject *sys_path;

void processCsv(const char csv_data[], const char selected_columns[], const char row_filter_definitions[]) {
    PyObject *pFunc = PyObject_GetAttrString(pModule, "process_csv_data");
    if (PyCallable_Check(pFunc)) {
        PyObject *pArgs = Py_BuildValue("(sss)", csv_data, selected_columns, row_filter_definitions);
        PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
        Py_DECREF(pArgs);
        if (pValue != NULL) {
            printf("%s", PyUnicode_AsUTF8(pValue));
            Py_DECREF(pValue);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
    }
    Py_DECREF(pFunc);
}

void processCsvFile(const char csv_file_path[], const char selected_columns[], const char row_filter_definitions[]) {
    PyObject *pFunc = PyObject_GetAttrString(pModule, "process_csv_file");
    if (PyCallable_Check(pFunc)) {
        PyObject *pArgs = Py_BuildValue("(sss)", csv_file_path, selected_columns, row_filter_definitions);
        PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
        Py_DECREF(pArgs);
        if (pValue != NULL) {
            printf("%s", PyUnicode_AsUTF8(pValue));
            Py_DECREF(pValue);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
    }
    Py_DECREF(pFunc);
}

__attribute__((constructor))
void init() {
    Py_Initialize();
    sys_path = PySys_GetObject("path");
    PyList_Append(sys_path, PyUnicode_FromString("src"));
    pModule = PyImport_ImportModule("libcsv");
    if (!pModule) {
        PyErr_Print();
    }
}

__attribute__((destructor))
void cleanup() {
    Py_DECREF(pModule);
    Py_Finalize();
}
