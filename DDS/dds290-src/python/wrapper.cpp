
#include "Python.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/dll.h"
#include "hands.h"


static void show_deal(char* pbn)
{
   ddTableDealPBN tableDealPBN;
   char line[80];

   strncpy(tableDealPBN.cards, pbn, 80);

   PrintPBNHand(line, tableDealPBN.cards);
}


static void calc_dd_table(char* pbn, ddTableResults* table)
{
    ddTableDealPBN tableDealPBN;

    int res;
    char line[80];
    bool match = true;

    strncpy(tableDealPBN.cards, pbn, 80);

    res = CalcDDtablePBN(tableDealPBN, table);

    if (res != RETURN_NO_FAULT)
    {
      ErrorMessage(res, line);
      match = false;
    }

    sprintf(line, "CalcDDtable: %s\n", (match ? "OK" : "ERROR"));
}

static void solve_board(char* pbn, 
                        int trump, 
                        int first, 
                        int first_card_suit, 
                        int first_card_rank, 
                        int target, 
                        int solutions, 
                        int mode)
{
    dealPBN dlPBN;
    futureTricks fut;

    int threadIndex = 0;
    int res;
    char line[80];

    dlPBN.trump = trump;
    dlPBN.first = first;
    dlPBN.currentTrickSuit[0] = first_card_suit;
    dlPBN.currentTrickSuit[1] = 0;
    dlPBN.currentTrickSuit[2] = 0;
    dlPBN.currentTrickRank[0] = first_card_rank;
    dlPBN.currentTrickRank[1] = 0;
    dlPBN.currentTrickRank[2] = 0;

    strncpy(dlPBN.remainCards, pbn, 80);

    res = SolveBoardPBN(dlPBN, target, solutions, mode, &fut, threadIndex);

    if (res != RETURN_NO_FAULT)
    {
        ErrorMessage(res, line);
        printf("DDS error: %s\n", line);
    }

    PrintFut("", &fut);
}

typedef struct {
    PyObject_HEAD
    ddTableResults* results;
}  TableResultsObject;

static void
TableResults_dealloc(TableResultsObject *self)
{
    Py_XDECREF(self->results);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
TableResults_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    TableResultsObject *self;
    self = (TableResultsObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->results = (ddTableResults*)malloc(sizeof(ddTableResults));
        if (self->results == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject *) self;
}


static PyObject *
TableResults_data(TableResultsObject *self, PyObject *args, PyObject *kwds)
{
    if (self->results == NULL) {
        PyErr_SetString(PyExc_AttributeError, "results");
        return NULL;
    }

    long i;
    long j;

    if (!PyArg_ParseTuple(args, "ll", &i, &j)) {
        return NULL;
    }

    return PyLong_FromLong(self->results->resTable[i][j]);
}

static PyMethodDef TableResults_methods[] = {
    {"data", (PyCFunction) TableResults_data, METH_VARARGS,
     "Return the number of xx, for a trump or NT and a player"
    },
    {NULL}  /* Sentinel */
};

/*
static PyTypeObject TableResultsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "dds.TableResult",
    .tp_basicsize = sizeof(TableResultsObject),
	.tp_itemsize = 0,
	.tp_dealloc = (destructor) TableResults_dealloc,
	//.tp_repr = NULL
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "TableResult objects",
   
//    .tp_members = TableResults_members,
    .tp_methods = TableResults_methods,
	
	.tp_new = TableResults_new,
};
*/

static PyTypeObject TableResultsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "dds.TableResult", // tp_name
    sizeof(TableResultsObject), // tp_basicsize
	0, // tp_itemsize
	(destructor) TableResults_dealloc, // tp_dealloc
	0, // vectorcall_offset
	0, // getattr
	0, // setattr
	0, // as_sync
	NULL,   // tp_repr
	0, // as_number
	0, // as_sequence
	0, // as_mapping
	0, // hash
	0, // call
	0, // str
	0, // getattro
	0, // setattro
	0, // as_buffer
    Py_TPFLAGS_DEFAULT, // tp_flags
	"TableResult objects", // tp_doc
	0, // traverse
	0, // clear
	0, // richcompare
	0, // weaklistoffset
	0, // iter
	0, // iternext
	TableResults_methods, // tp_methods
	0, //    .tp_members = TableResults_members,
	0, // getset
	0, // base
	0, // dict
	0, // descr_get
	0, // descr-set
	0, // dict_offset
	0, // int
	0, // alloc
	TableResults_new, // tp_new
};

static PyObject* py_show_deal(PyObject* self, PyObject* args)
{
    char* PBN;

    if (!PyArg_ParseTuple(args, "s", &PBN))
      return NULL;
  
    show_deal(PBN);

    Py_RETURN_NONE;
}

static PyObject* py_calc_dd_table(PyObject* self, PyObject* args)
{
    char* pbn;

    if (!PyArg_ParseTuple(args, "s", &pbn))
      return NULL;
  
    ddTableResults* results = new ddTableResults;
    calc_dd_table(pbn, results);

    TableResultsObject* o = PyObject_NEW(TableResultsObject, &TableResultsType);
    o->results = results;

    return (PyObject*)o;
}

static PyObject* py_show_results(PyObject* self, PyObject* args)
{
    TableResultsObject* res;

    if (!PyArg_ParseTuple(args, "O", &res))
      return NULL;
  
    PrintTable(res->results);

    Py_RETURN_NONE;
}

static PyObject* py_solve_board(PyObject* self, PyObject* args)
{
    char* pbn;
    long trump;
    long first;
    long first_card_suit;
    long first_card_rank;
    long target;
    long solutions;
    long mode;

    if (!PyArg_ParseTuple(args, "slllllll", &pbn, 
                                 &trump, 
                                 &first, 
                                 &first_card_suit, 
                                 &first_card_rank, 
                                 &target, 
                                 &solutions,
                                 &mode))
      return NULL;
  
    solve_board(pbn, trump, first, first_card_suit, first_card_rank, target, solutions, mode);

    Py_RETURN_NONE;
}

static PyMethodDef myMethods[] = {
   { "show_deal", py_show_deal, METH_VARARGS, "display PBN" },
   { "calc_dd_table", py_calc_dd_table, METH_VARARGS, "calc dd table PBN" },
   { "show_results", py_show_results, METH_VARARGS, "show_results DDS" },
   { "solve_board", py_solve_board, METH_VARARGS, "solve board PBN" },
   { NULL, NULL, 0, NULL }
};

static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "dds",
    "Test DDS",
    -1,
    myMethods
};

PyMODINIT_FUNC PyInit_dds(void)
{
    PyObject *m;
 
    if (PyType_Ready(&TableResultsType) < 0)
        return NULL;

    m = PyModule_Create(&myModule);

    if (m == NULL)
        return NULL;

    Py_INCREF(&TableResultsType);

    if (PyModule_AddObject(m, "TableResults", (PyObject *) &TableResultsType) < 0) {
        Py_DECREF(&TableResultsType);
        Py_DECREF(m);
        return NULL;
    }

    /* Adding module globals */
    if (PyModule_AddIntConstant(m, "SPADES", 0)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "HEARTS", 1)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "DIAMONDS", 2)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "CLUBS", 3)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "NOTRUMP", 4)) {
        Py_XDECREF(m);
        m = NULL;
    }

    if (PyModule_AddIntConstant(m, "NORTH", 0)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "EAST", 1)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "SOUTH", 2)) {
        Py_XDECREF(m);
        m = NULL;
    }
    if (PyModule_AddIntConstant(m, "WEST", 3)) {
        Py_XDECREF(m);
        m = NULL;
    }

#if defined(__linux) || defined(__APPLE__)
    SetMaxThreads(0);
#endif

  return m;
}



