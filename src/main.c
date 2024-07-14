#include <Python.h>
#include <stdio.h>

#include "../libcsv.h"

static PyObject *pModule;
static PyObject *sys_path;

/**
 * Process CSV data using the Python function `process_csv_data`.
 *
 * @param csv The CSV data to be processed.
 * @param selectedColumns The columns to be selected from the CSV data.
 * @param rowFilterDefinitions The filters to be applied to the CSV data.
 *
 * @return void
 * @throws None
 */
void processCsv(const char csv[], const char selectedColumns[],
                const char rowFilterDefinitions[]) {
  PyObject *pFunc = PyObject_GetAttrString(pModule, "process_csv_data");
  PyObject *pArgs = Py_BuildValue("(sss)", csv, selectedColumns, rowFilterDefinitions);
  PyObject *pValue = PyObject_CallObject(pFunc, pArgs);

  Py_DECREF(pFunc);
  Py_DECREF(pArgs);

  if (pValue != NULL) {
    printf("%s", PyUnicode_AsUTF8(pValue));
    Py_DECREF(pValue);
  } else {
    PyErr_Print();
  }
}

/**
 * Process a CSV file using the Python function `process_csv_file`.
 *
 * @param csvFilePath The file path of the CSV to be processed.
 * @param selectedColumns The columns to be selected from the CSV data.
 * @param rowFilterDefinitions The filters to be applied to the CSV data.
 *
 * @return void
 * @throws None
 */
void processCsvFile(const char csvFilePath[], const char selectedColumns[],
                    const char rowFilterDefinitions[]) {
  PyObject *pFunc = PyObject_GetAttrString(pModule, "process_csv_file");
  PyObject *pArgs = Py_BuildValue("(sss)", csvFilePath, selectedColumns,
                                  rowFilterDefinitions);
  PyObject *pValue = PyObject_CallObject(pFunc, pArgs);

  Py_DECREF(pFunc);
  Py_DECREF(pArgs);

  if (pValue != NULL) {
    printf("%s", PyUnicode_AsUTF8(pValue));
    Py_DECREF(pValue);
  } else {
    PyErr_Print();
  }
}

/**
 * Initializes the Python interpreter and adds the "src" directory to the system
 * path.
 *
 * This function is called automatically before the program starts executing. It
 * initializes the Python interpreter using `Py_Initialize()` and retrieves the
 * system path using `PySys_GetObject("path")`. It then appends the "src"
 * directory to the system path using `PyList_Append()` and
 * `PyUnicode_FromString()`. Finally, it imports the "libcsv" module using
 * `PyImport_ImportModule()` and checks if the module was successfully imported.
 * If the module was not imported, it prints the error using `PyErr_Print()`.
 *
 * @throws None
 */
__attribute__((constructor)) void init() {
  Py_Initialize();
  sys_path = PySys_GetObject("path");
  PyList_Append(sys_path, PyUnicode_FromString("src"));
  pModule = PyImport_ImportModule("libcsv");
  if (!pModule) {
    PyErr_Print();
  }
}

// Cleans up resources used by the program, specifically decreasing the
// reference count of the Python module and finalizing the Python interpreter.
__attribute__((destructor)) void cleanup() {
  Py_DECREF(pModule);
  Py_Finalize();
}
