## Exploring Multi-Modal Integration with Tool-Augmented LLM Agents for Precise Causal Discovery

### First Iteration:

#### Abstract:

- *semantic cues* 

- Issue: development of LLMs for causal discovery lags behind other areas
  
  - (*question*) non-knoledge driven causal discovery

- MATMCD: a multi-agent system powered by tool-augmented LLMs
  
  - Two key agents: 
    
    - Data Augmentation agent: retrieve and process modality-augmented data, 
    
    - Causal Constraint agent: integrates multi-modal data for knowledge-driven inference

- "How to construct an accurate causal graph?"

- The problem of *multi-modality enhanced causal discovery* via LLM agents

#### Conclusion:

- The tool-augmented LLMs are designed for integrating text data with graphs+





### Second Iteration:

#### Related work

- Causal Discovery Methods: conventional data-driven SCD (Slowly Chaning Dimension) algorithms
  
  - non-parametric
  
  - semi-parametric

- Knowledge-driven methods (newly-found promising for causal discovery)

- Still, no exploration on the potential of multi-modal data in the LLM-based causal discovery process

- Primary categories of multi-agent systems: 
  
  - Cooperative agents (paper focus)
  
  - Competitive agents
  
  - Debating agents



#### Methodology

- MATMCD system:
  
  - Goal of MATMCD: **infer accurate causal relationships in $\Epsilon$ among the set of $n$ variables in $V$**.
  
  - Causal Graph Estimator
    
    - an initializer of causal graph, built upon data-driven SCD algo.
    
    - Three SCD algos: 
      
      - Constrained-based Method: Peter-Clark (PC) algo
      
      - Score-based method: Exact Search (ES) algo
      
      - Constrained functional causal models DirectLiNGAM (semi-parametric)
  
  - Data Augmentation Agent
    
    - retrieve semantics-rich contextual data pertinent to hte intial causal graph.
    
    - Comprises a Search LLM and a Summary  LLM
      
      - Search LLM: access to a set of tools for data search
        
        - Extendable for wide scenarios by inclduing other application-specific tools.
        
        - store/record teh call as *calling history memory* to reduce redundant queries.
        
        - "can we 'tree' the history for a quicker search?"
      
      - Summary LLM: 
        
        - Summarize *Retrieved Data* from Search LLM: 
          
          - description of dataset
          
          - relationships between variables (using RAG for an efficient summarization to avoid exceeding context window of the LLM)
            
            - data divided into indexed doc chunks (implemented by LlamaIndex)
          
          - Conduct thorough screening in RAG of the Retrieved Data Memory to prevent info leak when retrieving web content.  
  
  - Causal Constraint Agent
    
    - based on the Two-Stage Prompting framework of zero-shot CoT (*citation* Kojima et al., 2022)
      
      - A prompt builder with contextual data from DA agent to prompt a KNowledge LLM
        
        - The knowledge LLM is tasked with explaining each (non-)existing causal reelationship in the initial causal graph $G_0$ based on the contextual data nad its own knolwedge. 
      
      - Top-K-Guess to address potential uncertainty in the conclusions of existitence of each relationship
  
  - Causal Graph Refiner
    
    - Ensure the final causal graph G is acyclic. 
    
    - (*idea*) what if we build the graph firstly without making it directed, then we make the agents to propose multiple possible cases of directed and here, input the contextual data as prompt to decide and output the final DAG: 
      
      1. We make the relation non-directed, in other word, $v_i$ and $v_j$ are related, rather than $v_i$ leads to $v_j$, when constructing the initial graph $G_0$, which means in this step, we care more about the existance of the relationship between two variables.  
      
      2. Based on the init graph, propose directed versions
      
      3. DA-agent and CC-agent to ensure the Causal constraints to select the best one among the drafts
      
      4. Refiner for refining the chosen one from last step
      
      5. the firnal Causal Graph $G$  
  
  - Key novelty of MATMCD: exploration of DA-Agent for multi-modal enhancement of causal discovery. 


