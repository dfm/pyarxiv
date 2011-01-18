#include <Python.h>
#include <numpy/arrayobject.h>
#include <btparse.h>

/* ====================== //
// PYTHON INITIALIZATIONS //
// ====================== */

PyMODINIT_FUNC init_C_btparse(void);
static PyObject *btparse_load(PyObject *self, PyObject *args);

static PyMethodDef btparse_methods[] = {
    {"load", btparse_load, METH_VARARGS,"Load bibtex from a file."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_C_btparse(void)
{
    PyObject *m;

    m = Py_InitModule("_C_btparse", btparse_methods);
    if (m == NULL)
        return;

    import_array(); /* numpy import */
}



/* ================ //
// MODULE FUNCTIONS //
// ================ */

static PyObject *btparse_load(PyObject *self, PyObject *args)
{
    /* parse inputs */
    PyObject *str = NULL;
    if (!PyArg_ParseTuple(args, "S", &str)) goto fail;
    char *infn = PyString_AsString(str);
    if (infn == NULL) goto fail;
        
    /* list that we will return */
    PyObject *list = PyList_New(0);
    if (list == NULL) goto fail;
    
    /* start btparse */
    bt_initialize();
    
    AST *entry;
    int ok, i;
    ushort options = BTO_NOSTORE;
    
    /* open input .bib file */
    FILE *infile = fopen(infn,"r");
    if (infile == NULL) {
        PyErr_SetObject(PyExc_RuntimeError, PyString_FromFormat("cannot open file: %s",infn));
        return NULL;
    }
    
    /* month macros --- this is klugey as fuck! */
    bt_add_macro_text("jan","jan",NULL,0);
    bt_add_macro_text("feb","feb",NULL,0);
    bt_add_macro_text("mar","mar",NULL,0);
    bt_add_macro_text("apr","apr",NULL,0);
    bt_add_macro_text("may","may",NULL,0);
    bt_add_macro_text("jun","jun",NULL,0);
    bt_add_macro_text("jul","jul",NULL,0);
    bt_add_macro_text("aug","aug",NULL,0);
    bt_add_macro_text("sep","sep",NULL,0);
    bt_add_macro_text("oct","oct",NULL,0);
    bt_add_macro_text("nov","nov",NULL,0);
    bt_add_macro_text("dec","dec",NULL,0);
    
    /* load entries from the .bib file */
    bt_set_stringopts(BTE_COMMENT, BTO_COLLAPSE);
    while (entry = bt_parse_entry(infile, NULL, options, &ok))
    {
        if (ok)
        {
            /* new dictionary */
            PyObject *dict = PyDict_New();
            if (dict == NULL) {
                Py_XDECREF(list);
                PyErr_SetString(PyExc_RuntimeError, "couldn't allocate new dict object");
                return NULL;
            }
            
            AST *field = NULL;
            char *field_name = malloc(4000*sizeof(char));
            while (field = bt_next_field(entry, field, &field_name))
            {
                PyObject *key = PyString_FromString(field_name);
                PyObject *val = PyString_FromString(bt_get_text(field));
                PyDict_SetItem(dict, key, val);
                printf("%s\n",bt_get_text(field));
            }
            free(field_name);
            if (PyDict_Size(dict) > 0)
                PyList_Append(list,dict);
        }
    }
    fclose(infile);
    bt_cleanup();
    /* end btparse */
    
    Py_INCREF(list);
    return list;

fail:
    PyErr_SetString(PyExc_RuntimeError, "couldn't parse input");
    return NULL;
}

