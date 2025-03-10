## Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference

- idea: a small portion of tokens can dominate the accuracy of token generation ---> loading the cirtical tokens only

- question: how to identify critical portions of KV cache?

- Quest: a KV cache accerleration algorithm which exploits query-aware sparsity
  
  - retain all of KV cache
  
  - select part of the cache based on *currenty query* for acceleration.
  
  - "*in order not to miss critical tokens, we should select pages containing the token with the highest attention weights*"
    
    - using the upper bound attention weights. 

- issue of current methods on accelerating KV cache: discarding tokens might be important for future tokens ---> loss of important info

- Workflow: 
  
  - Split KV cache into fixed-size pages
  
  - For each page, store the min and max values of each feature dimension in the Key vectors
  
  - For new query Q, compute an upper-bound estimate of the attention contribution for each page (critical score/criticality)
  
  - Select Top-K pages with the highest critical scores
  
  - Load only the selected pages from the KV cache and compute the attention scores on them for generating next token. 
    
    

## H$_2$O: Heavy-Hitter Oracle for Effificient Generative Inference of Large Language Models

- An observation: *a small portion of tokens (A.K.A. Heavy-Hitters or H$_2$ in this paper) contributes most of the value when computing attention scores* 

- H$_2$O: a KV cache eviction policy that dynamically retains a balance of recent and H$_2$ tokens.

- Challenge: reduce the KV cache memory footprints in LLMS without accuracy drops.

- Their Goal on KV cache: 
  
  - Small cache size: Sparsity
  
  - Low miss rate: Heavy-hitters
  
  - Low cost eviction policy: Greedy algorithm
  
  - H$_2$O focuses on the efficiency of KV cache in attention during the *token generation* phase to accelerate LLM inference. 





## FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

- Definition: An *IO-aware exact attention algorithm* that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory and GPU on-chip SRAM

- Avoid reading and writing the attention matrix to and from HBM:
  
  - Split input into blocks: **tilling**
  
  - store the softmax normalization factor from the forward pass to quickly recompute attention on-chip in hte backward pass.

- ![26721462-2966-4e48-9183-ef3f6e609aa9](file:///C:/Users/llxCl/OneDrive/%E5%9B%BE%E7%89%87/Typedown/26721462-2966-4e48-9183-ef3f6e609aa9.png)

## 
