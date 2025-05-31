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

try:
    lib = ctypes.CDLL("./libkdtree.dll")
except OSError as e:
    print(f"Erro ao carregar a biblioteca ./libkdtree.dll: {e}")
    print("Certifique-se de que a biblioteca (libkdtree.dll) foi compilada e está no local correto e com a arquitetura correta (32bit/64bit).")
    print("Exemplo de compilação (MinGW): gcc -shared -o libkdtree.dll kdtree.c -lm")
    exit(1)

lib.kdtree_construir_global.argtypes = []
lib.kdtree_construir_global.restype = None

lib.inserir_ponto_global.argtypes = [TReg]
lib.inserir_ponto_global.restype = None

lib.buscar_mais_proximo_global.argtypes = [TReg]
lib.buscar_mais_proximo_global.restype = TReg

lib.get_tree_global.argtypes = []
lib.get_tree_global.restype = POINTER(Tarv)