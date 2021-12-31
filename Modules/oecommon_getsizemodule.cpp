#include <iostream>
//#include <experimental/filesystem>
#include <filesystem>
#define PY_SSIZE_T_CLEAN
#include <Python.h>


//namespace fs = std::filesystem;
static PyObject * get_directory_size(PyObject *self, PyObject *args) {
    const char *command;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;

    uintmax_t total_size = 0;
    for (const std::filesystem::directory_entry &p: std::filesystem::recursive_directory_iterator(command)) {
        if (std::filesystem::is_regular_file(p.path())) {
            total_size += p.file_size();
        }
    }
    return PyLong_FromUnsignedLongLong(total_size);
}

static PyMethodDef GetSizeMethods[] = {
        {"get_directory_size",  get_directory_size, METH_VARARGS, "Get directory size"},
        {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef oecommon_getsizemodule = {
        PyModuleDef_HEAD_INIT,
        "getsize",   /* name of module */
        NULL, /* module documentation, may be NULL */
        -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
        GetSizeMethods
};

PyMODINIT_FUNC
PyInit_oecommon_getsize(void)
{
    return PyModule_Create(&oecommon_getsizemodule);
}
