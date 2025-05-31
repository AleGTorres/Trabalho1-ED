#include<stdio.h>
#include<stdlib.h>
#include<float.h>
#include<string.h>
#include<assert.h>
#include<math.h>

#define K_DIMENSIONS 128

typedef struct _reg{
    float embedding[K_DIMENSIONS];
    char id_pessoa[100];
}treg;

void * aloca_reg(const float embedding[K_DIMENSIONS], const char id_pessoa[]){
    treg * reg = (treg *)malloc(sizeof(treg));
    if (!reg) {
        perror("Falha ao alocar treg");
        exit(EXIT_FAILURE);
    }
    memcpy(reg->embedding, embedding, K_DIMENSIONS * sizeof(float));
    strncpy(reg->id_pessoa, id_pessoa, 99);
    reg->id_pessoa[99] = '\0';
    return reg;
}

int comparador(void *a, void *b, int pos){
    treg *reg_a = (treg *)a;
    treg *reg_b = (treg *)b;
    
    int dimension_index = pos % K_DIMENSIONS;

    if (reg_a->embedding[dimension_index] < reg_b->embedding[dimension_index]) {
        return -1;
    } else if (reg_a->embedding[dimension_index] > reg_b->embedding[dimension_index]) {
        return 1;
    } else {
        return 0;
    }
}

double distancia(void * a, void *b){
    treg *reg_a = (treg *)a;
    treg *reg_b = (treg *)b;
    double sum_sq_diff = 0.0;
    for (int i = 0; i < K_DIMENSIONS; ++i) {
        double diff = reg_a->embedding[i] - reg_b->embedding[i];
        sum_sq_diff += diff * diff;
    }
    return sum_sq_diff;
}

typedef struct _node{
    void * key;
    struct _node * esq;
    struct _node * dir;
}tnode;

typedef struct _arv{
    tnode * raiz;
    int (*cmp)(void *, void *, int);
    double (*dist) (void *, void *);
    int k;
}tarv;


void kdtree_constroi(tarv * arv, int (*cmp)(void *a, void *b, int ),double (*dist) (void *, void *),int k_dims){
    arv->raiz = NULL;
    arv->cmp = cmp;
    arv->dist = dist;
    arv->k = k_dims;
}

void test_constroi(){
    tarv arv;
    tnode node1, node2;
    
    float emb1[K_DIMENSIONS];
    float emb2[K_DIMENSIONS];
    for(int i=0; i<K_DIMENSIONS; ++i) {
        emb1[i] = (float)i;
        emb2[i] = (float)i * 2.0f;
    }

    node1.key = aloca_reg(emb1, "Pessoa1");
    node2.key = aloca_reg(emb2, "Pessoa2");

    kdtree_constroi(&arv, comparador, distancia, K_DIMENSIONS);
    
    assert(arv.raiz == NULL);
    assert(arv.k == K_DIMENSIONS);
    ((treg*)node1.key)->embedding[0] = 1.0f;
    ((treg*)node2.key)->embedding[0] = 2.0f;
    assert(arv.cmp(node1.key, node2.key, 0) == -1);

    ((treg*)node1.key)->embedding[1] = 5.0f;
    ((treg*)node2.key)->embedding[1] = 2.0f;
    assert(arv.cmp(node1.key, node2.key, 1) == 1);


    assert(strcmp(((treg *)node1.key)->id_pessoa, "Pessoa1") == 0);
    assert(strcmp(((treg *)node2.key)->id_pessoa, "Pessoa2") == 0);
    
    printf("Testes de construção básicos passaram (necessário adaptar para embeddings).\n");
    free(node1.key);
    free(node2.key);
}

void _kdtree_insere(tnode **raiz, void * key, int (*cmp)(void *a, void *b, int), int profund, int k){
    if(*raiz == NULL){
        *raiz = (tnode*)malloc(sizeof(tnode));
        if (!*raiz) {
            perror("Falha ao alocar tnode para inserção");
            exit(EXIT_FAILURE);
        }
        (*raiz)->key = key;
        (*raiz)->esq = NULL;
        (*raiz)->dir = NULL;
    }else{
        int pos = profund % k;
        if (cmp(key, (*raiz)->key, pos) < 0){
            _kdtree_insere(&((*raiz)->esq), key, cmp, profund + 1, k);
        }else{
            _kdtree_insere(&((*raiz)->dir), key, cmp, profund + 1, k);
        }
    }
}

void kdtree_insere(tarv *arv, void *key){
    _kdtree_insere(&(arv->raiz), key, arv->cmp, 0, arv->k);
}


void _kdtree_destroi(tnode * node){
    if (node!=NULL){
        _kdtree_destroi(node->esq);
        _kdtree_destroi(node->dir);
        free(node->key);
        free(node);
    }
}

void kdtree_destroi(tarv *arv){
    _kdtree_destroi(arv->raiz);
    arv->raiz = NULL;
}

void _kdtree_busca(tarv *arv, tnode * atual_node, void * query_key, int profund, double *menor_dist, tnode **menor_node){
    if (atual_node == NULL) {
        return;
    }

    double dist_atual = arv->dist(atual_node->key, query_key);

    if (dist_atual < *menor_dist) {
        *menor_dist = dist_atual;
        *menor_node = atual_node;
    }

    int dimension_index = profund % arv->k;

    tnode *lado_principal, *lado_oposto;

    if (arv->cmp(query_key, atual_node->key, profund) < 0) { 
        lado_principal = atual_node->esq;
        lado_oposto = atual_node->dir;
    } else {
        lado_principal = atual_node->dir;
        lado_oposto = atual_node->esq;
    }

    _kdtree_busca(arv, lado_principal, query_key, profund + 1, menor_dist, menor_node);

    double diff_dim_atual = ((treg*)query_key)->embedding[dimension_index] - ((treg*)atual_node->key)->embedding[dimension_index];
    double dist_ao_plano_sq = diff_dim_atual * diff_dim_atual;

    if (dist_ao_plano_sq < *menor_dist) {
        _kdtree_busca(arv, lado_oposto, query_key, profund + 1, menor_dist, menor_node);
    }
}

tnode * kdtree_busca(tarv *arv, void * query_key){
    if (arv->raiz == NULL) return NULL;
    tnode * menor_node = NULL;
    double menor_dist = DBL_MAX;
    _kdtree_busca(arv, arv->raiz, query_key, 0, &menor_dist, &menor_node);
    return menor_node;
}

tarv arvore_global;

void kdtree_construir_global() {
    kdtree_constroi(&arvore_global, comparador, distancia, K_DIMENSIONS);
    printf("Árvore KD global inicializada com K=%d dimensões.\n", K_DIMENSIONS);
}

void inserir_ponto_global(treg ponto_reg) {
    treg *novo_ponto_heap = (treg*)malloc(sizeof(treg));
    if (!novo_ponto_heap) {
        perror("Falha ao alocar memória para novo_ponto_heap em inserir_ponto_global");
        return;
    }
    memcpy(novo_ponto_heap->embedding, ponto_reg.embedding, K_DIMENSIONS * sizeof(float));
    strncpy(novo_ponto_heap->id_pessoa, ponto_reg.id_pessoa, 99);
    novo_ponto_heap->id_pessoa[99] = '\0';
    
    kdtree_insere(&arvore_global, novo_ponto_heap); 
}

treg buscar_mais_proximo_global(treg query_reg) {
    tnode *menor_encontrado_node = kdtree_busca(&arvore_global, &query_reg);
    
    if (menor_encontrado_node != NULL && menor_encontrado_node->key != NULL) {
        return *((treg *)(menor_encontrado_node->key));
    } else {
        treg not_found_reg; 
        memset(&not_found_reg, 0, sizeof(treg));
        strcpy(not_found_reg.id_pessoa, "NOT_FOUND"); 
        return not_found_reg;
    }
}

tarv* get_tree_global() {
    return &arvore_global;
}

void test_busca(){
    tarv arv_teste;
    kdtree_constroi(&arv_teste, comparador, distancia, K_DIMENSIONS);

    float emb_a[K_DIMENSIONS], emb_b[K_DIMENSIONS], emb_c[K_DIMENSIONS];
    for(int i=0; i < K_DIMENSIONS; ++i) {
        emb_a[i] = (float)i + 1.0f;
        emb_b[i] = (float)i + 10.0f;
        emb_c[i] = (float)i + 5.0f;
    }

    kdtree_insere(&arv_teste, aloca_reg(emb_a, "PessoaA"));
    kdtree_insere(&arv_teste, aloca_reg(emb_b, "PessoaB"));
    kdtree_insere(&arv_teste, aloca_reg(emb_c, "PessoaC"));

    printf("\nIniciando teste de busca...\n");

    treg query_reg;
    for(int i=0; i < K_DIMENSIONS; ++i) query_reg.embedding[i] = (float)i + 1.1f;
    strcpy(query_reg.id_pessoa, "QueryPertoDeA");


    tnode * mais_proximo_node = kdtree_busca(&arv_teste, &query_reg);
    if (mais_proximo_node && mais_proximo_node->key) {
        printf("QueryPertoDeA - Vizinho mais próximo: %s\n", ((treg*)mais_proximo_node->key)->id_pessoa);
        assert(strcmp(((treg *)mais_proximo_node->key)->id_pessoa, "PessoaA") == 0);
    } else {
        printf("QueryPertoDeA: Nenhum vizinho encontrado.\n");
        assert(0);
    }
    
    for(int i=0; i < K_DIMENSIONS; ++i) query_reg.embedding[i] = (float)i + 10.1f;
    strcpy(query_reg.id_pessoa, "QueryPertoDeB");
    mais_proximo_node = kdtree_busca(&arv_teste, &query_reg);
     if (mais_proximo_node && mais_proximo_node->key) {
        printf("QueryPertoDeB - Vizinho mais próximo: %s\n", ((treg*)mais_proximo_node->key)->id_pessoa);
        assert(strcmp(((treg *)mais_proximo_node->key)->id_pessoa, "PessoaB") == 0);
    } else {
        printf("QueryPertoDeB: Nenhum vizinho encontrado.\n");
        assert(0);
    }

    for(int i=0; i < K_DIMENSIONS; ++i) query_reg.embedding[i] = (float)i + 5.1f;
    strcpy(query_reg.id_pessoa, "QueryPertoDeC");
    mais_proximo_node = kdtree_busca(&arv_teste, &query_reg);
     if (mais_proximo_node && mais_proximo_node->key) {
        printf("QueryPertoDeC - Vizinho mais próximo: %s\n", ((treg*)mais_proximo_node->key)->id_pessoa);
        assert(strcmp(((treg *)mais_proximo_node->key)->id_pessoa, "PessoaC") == 0);
    } else {
        printf("QueryPertoDeC: Nenhum vizinho encontrado.\n");
        assert(0);
    }

    kdtree_destroi(&arv_teste);
    printf("Testes de busca concluídos.\n");
}

int main(void){
    printf("Iniciando main para testes locais...\n");
    
    printf("Testando inicialização da árvore global...\n");
    kdtree_construir_global();
    assert(arvore_global.raiz == NULL);
    assert(arvore_global.k == K_DIMENSIONS);
    assert(arvore_global.cmp == comparador);
    assert(arvore_global.dist == distancia);
    printf("Inicialização da árvore global OK.\n");

    printf("Testando inserção e busca na árvore global...\n");
    treg ponto_exemplo_api;
    for(int i=0; i < K_DIMENSIONS; ++i) ponto_exemplo_api.embedding[i] = (float)i + 2.5f;
    strcpy(ponto_exemplo_api.id_pessoa, "PessoaGlobal1");
    inserir_ponto_global(ponto_exemplo_api);

    assert(arvore_global.raiz != NULL);
    assert(strcmp(((treg*)arvore_global.raiz->key)->id_pessoa, "PessoaGlobal1") == 0);

    treg query_exemplo_api;
    for(int i=0; i < K_DIMENSIONS; ++i) query_exemplo_api.embedding[i] = (float)i + 2.6f;

    treg resultado_api = buscar_mais_proximo_global(query_exemplo_api);
    printf("Busca na árvore global por ponto próximo a 'PessoaGlobal1' encontrou: ID '%s'\n", resultado_api.id_pessoa);
    assert(strcmp(resultado_api.id_pessoa, "PessoaGlobal1") == 0);
    printf("Teste de inserção e busca na árvore global OK.\n");
    
    kdtree_destroi(&arvore_global); 

    test_constroi(); 
    test_busca();    
    
    printf("SUCCESS!! (após adaptação dos testes)\n");
    return EXIT_SUCCESS;
}