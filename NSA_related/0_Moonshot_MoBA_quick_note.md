### First iter:

#### Intro

key question: seeking a general, highly efficient way of utilizing the sparse attention.



(*question*) Mamba, a linear attention approach. similarly, RWKV, RetNet.

(*idea*) a design specifically for the linear attention architecture? including the pre and post training.



- Question of the paper: A attention architecture *retrains the Transformer framework*, while **adhering to a "less structure" principle, allowing the model to determine where to attend without relying on predefined biases**. 

- workflow: 
  
  - **Partitioning** the context into **blocks**
  
  - **Employing** a **gating mechanism** to **selectively route** query tokens to the most relevant blocks.

#### Method:

- MoBA architecture: 
  
  - Block Partitioning Strategy
  
  - Block Selection strategy
  
  - (*question*) top-k gating mechanism from MoE?
  
  - Affinity score $s_i$: measuring the relevance between query $q$ and the $i$-th block.

- Running Example: 
  
  - Causality Preservation: 
    
    - No Attention to Future Blocks
      
      - Attention scope = [current and past blocks]
    
    - Current Block Attention and Causal Masking
      
      - Query token should not access to the tokens behind itself within the "current block" since it will affect the "causality" ---- a token cannot influence tokens come before it.
  
  - MoBA key design: 
    
    - Fine-Grained Block Segmentation
    
    - Hybrid of MoBA and Full Attention.
      
      - key feature: MoBA maintains the same num of parameters, no addition/subtraction.
      
      - transitioning full attention to sliding window attention
    
    - Comparing to Sliding Window Attention and Attention Sink. 
      
      - Both can be considered as special cases of MoBA
      
      - SWA: MoBA witha a gating network that keeps selecting the most recent blocks.
      
      - Attn Sink: MoBA with a gating network that always selects both the initial and the recent blocks.
      
      - **MoBA can flexibly approximate many static sparse attention architectures by incorporating specific gating networks.**
  
  - Implementation: 
    
    - MoBA 5 steps: 
      
      - Determine the assignment of query tokens to KV blocks according to the gating network and causal mask.
      
      - Arrange the ordering of query tokens based on their assigned KV blocks.
      
      - Compute attention outputs for each KV block and the query tokens assigned to it. This step can be optimized by FlashAttention with varying lengths.
      
      - Compute attention outputs for each KV block and the query tokens assigned to it. This step can be optimized by FlashAttention with varying lengths.
      
      - Combine the corresponding attention outputs using online Softmax (i.e., tiling), as a query token may attend to its current block and multiple historical KV blocks
      
      - (*question*) online softmax
        
        - (*answer*) make the two-pass computation of standard softmax to one-pass: updating both the **running maximum** and **a runing total of exponentials**. 
          
          - maintains stability by constantly adjusting the sum relative to the running maximum
          
          - one-pass 
          
          - no need to store the entire vector in memory if the values are being processed in a streaming fashion. 

#### Experiments:

- (*question*) Chinchilla scaling law

- Trailing LM loss: computed by the LM loss of hte last few tokens in the sequence
  
  

#### Related Work:

- (*question*) Reformer

- (*question*) Routing Transformer; Locality-sensitive hashing (LSH)

- (*question*) Memorizing Transformers; Unlimiformer

- (*question*) CoLT5

- (*question*) Sparse Sinkhorn

- Prefill optimization phase: 
  
  - MoA
  
  - Minference
  
  - SeerAttention

- Decode optimization: 
  
  - TOVA
  
  - FastGen
  
  - Quest*: MoBA with a smaller block size and a specialized block representation function
  
  - Longheads: MoBA with a top-1 gating network

- Beyond Tranditional Attention Architecture: 
  
  - State Space Models (SSMs)
  
  - Linear Attention:
    
    - Hyena
    
    - Performer
    
    - Linformer
    
    - Mamba
    
    - RetNet
