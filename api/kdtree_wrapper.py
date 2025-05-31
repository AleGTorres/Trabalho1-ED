import ctypes
from ctypes import Structure, POINTER, c_float, c_int, c_char, CFUNCTYPE, c_double

K_DIMENSIONS = 128

class TReg(Structure):
    _fields_ = [("embedding", c_float * K_DIMENSIONS),
                ("id_pessoa", c_char * 100)
               ]

class TNode(Structure):
    pass

TNodePtr = POINTER(TNode)

TNode._fields_ = [("key", ctypes.c_void_p),
                  ("esq", TNodePtr),
                  ("dir", TNodePtr)]

CMPFUNC = CFUNCTYPE(c_int, ctypes.c_void_p, ctypes.c_void_p, c_int)
DISTFUNC = CFUNCTYPE(c_double, ctypes.c_void_p, ctypes.c_void_p)

class Tarv(Structure):
    _fields_ = [("raiz", TNodePtr),
                ("cmp", CMPFUNC),
                ("dist", DISTFUNC),
                ("k", c_int)
               ]

lib = ctypes.CDLL("./libkdtree.dll")


lib.kdtree_construir_global.argtypes = []
lib.kdtree_construir_global.restype = None

lib.inserir_ponto_global.argtypes = [TReg]
lib.inserir_ponto_global.restype = None

lib.buscar_mais_proximo_global.argtypes = [TReg]
lib.buscar_mais_proximo_global.restype = TReg

lib.get_tree_global.argtypes = []
lib.get_tree_global.restype = POINTER(Tarv)