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

## GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

- A mechanism or a more general respresentative of multi-heads attention (?)

- MHA (multi-head attention) = GQA_H (H = # of heads); MQA (multi-query attention) = GQA_1

- assign a sinlge KV pair with a block of queries, G = H/B_size 
  
  
  
  

## SpecInfer: Accelerating Large Language Model Serving with Tree-based Speculative Inference and Verification (Tree Attn)

- Two Challenges: 
  
  - Explore an extremely large search space of candidate token sequences to maximize speculative performance. 
    
    - Why so large?
      
      - modern LLMs generally involve large vocabularies
      
      - maximizing speculative performance requires predicting mltiple future tokens rather than next-one only
  
  - Verify the speculated tokens.
    
    - "*To preserve an LLM’s generative performance, SpecInfer must guarantee that its tree-based speculative inference and verification mechanism generates the next token by following the **exact same probability distribution** as incremental decoding*"
  
  - Mechanisms: 
    
    - multi-step speculative sampling
    
    - tree-based parallel decoding 
    
    - merge&expansion-based construction of token trees by exploiting diversity within and across SSMs
      
      - expansion-based for single SSM to predict an LLM's output
      
      - merge-based for multiple SSMs to predict an LLM's output
  
  - Token Tree Verifier: 
    
    - Tree Attention: generalize the attention mechanism from sequence to tree structure
      
      - Fore a token tree $N$ and a abitrary node $u \in N$, the tree attention is the **output of computing the original Transformer-based squence attention on $S_u$** 
        
        - $T_{REE}A_{TTENTION}(u) = A_{TTENTION}(S_u) \forall u \in N$ 
    
    - Tree-based parallel decoding
      
      - "two token sequences sharing a common prefix **have the same attention outpus** for the common prefix due to the *causal mask*" 

## Blockwise Parallel Transformers for Large Context Models

- A blockwise computation of self-attention and feedforward approach. 

- Memory cost on large feedforward layers has been overlooked.

- "Additionally, if there are overlaps (e.g., common prefixes), caching and reuse can further reduce redundant work."

- Workflow: 
  
  1. Split sequence into smaller blocks
  
  2. For each block, compute the attention
  
  3. Feed the output of step 2 into the FFN block by block
  
  4. Scale the outputs from FFN 
  
  5. Concatenate the scaled outputs to obtain the final output.
     
     
     
     

## MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention *

- Specifically for long-context scenarios with minimal overhead.

- Three general patterns of sparse attention in long-context LLMs
  
  - A-shape pattern
  
  - Vertical-Slash pattern
  
  - Block-Sparse Pattern

- A dynamic sparse mask for each head 





## Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

- CoT: a series of intermediate natrual language reasoning steps that  that lead to the final output.

- Benefit the ability of large models to solve reasoning related problems. 

- No gaurantee on the correctness of CoT. 

- How to make it appear on small models?
