### First Iteration

- Abstract
  
  - (question) why the typical decdoing method requires a separate forward pass through the model for each token generated?
    
    - (answer) because for each new token, the context would include the last generated token and previous prompt, and the model will need to use all the context as input to compute the new probability distribution for next token.
  
  - *Limitation*: inefficencies and resource demands.
  
  - *Existing approaches*: 
    
    - fine-tuning smaller models ---> resource-intensive (why?)
      
      - (answer) this means using a smaller auxiliary model to generate draft tokens that are later verified by the main larger model. Thus need to fine-tuing the smaller model to match the larger one's behavior, which can be resource intensive. (e.g., *Speculative Decoding*)  
      
      - (idea) I feel that there is a potential waste of the model capacity in speculative decoding: treating the larger model as a verifier and only allow it to modify the generated token block when rejecting seems an inefficient way to utilize the larger model.
    
    - relying on fixed retrival schems to construct drafts for the next tokens ---> lack adaptability and fail to generalize across different models and contexts
  
  - *ADED*: accelerating LLM decoding without requiring fine-tuning
    
    - an adaptive drafte verification process --> imporve efficiency
    
    - tri-gram matrix-based LLM representation to dynamically approximate the output distribution of LLM ---> adjust to changing token probabilities during decoding 
    
    - a draft construction mechanism to balance exploration and exploitation ---> outputs are diverse with "high likelihood"
    
    - result: a faster and more accurate decoding
      
      - (question) how "accurate" and "faster"?
  
  - (question) what the hec with decoding? is it so complicated?
    
    - (answer) yeah it is, because the decoding step includes the part of next-token prediction and convertion from tokens to human language

- Introduction
  
  - "fine-tuning free draft-verification"
  
  - "How to design an adaptive draft construction process that can evolve itself and accurately approximate LLM outputs during decoding?"
  
  - contribution: 
    
    - **tri-gram matrix-based representation** to *approximate the LLM output distribution* and *enhance adaptability*
    
    - **draft maker** to *balance exploration and exploitation* for high-quality drafts.
    
    - 2.5X speedup in latency; 20% avg improvement on acceptance rate

- Conclusion: 
  
  - "using a tri-gram matrix and enhances draft quality though MCTS, eliminating the need for fine-tuning"
  
  - potential limitations in extremely large-scale deploments
    
    
    
    
    
    

### Second Iteration

- Keys:
  
  - draft maker
  
  - tri-gram
  
  - PUCT
  
  - tree attention
  
  - MCTS
    
    - The way how we calculate the UCB determines that this method will grade the path/choice which is explored less a higher score to balance the exploration on different paths ---> (diversity?)
  
  - Lookahead decoding

- (question) for adaptivity, will the corpus be fixed or not during the process?

- (question) how do you ensure the approximation is good enough when distilling linguistic knowledge from the corpus.

- (question) how do you guarantee that the corpus would represent the output distribution of the LLM?

- (question) why would utilizing MCTS to guide the search process of drafts of the next tokens helpful? 

- (idea) combination of _medusa_ and _ADED_?
  
  

### Insertion

- Target: 
  
  - An adaptive draft construction process
    
    - for draft construction
    
    - evolve itself (adaptivity)
    
    - accurately approximate LLM outputs during decoding (accuracy)

- Keys: 
  
  - A draft maker inspired by Monte Carlo Tree Search
    
    - Goal: balance the exploration and exploitation
    
    - Trick: use a token preference score to maintain the balance during *search process*
  
  - Token preference score in draft maker
    
    - Goal: main the balance
    
    - Components: 
      
      - First part: based on the approximate conditional probability distribution of hte next token obtained from LLM representative
        
        - Idea: reflecting the draft maker's current knowledge of the LLM  (a representation of **exploitation**)
      
      - Second part: 
        
        - Goal: encourage the draft maker to explore unexplored/less explored draft spaces
  
  - **LLM representative**
    
    - what is it actually?
      
      - The tri-gram matrix, it stores the a combination of tri-tokens, which the first two can be considered like an input, and the third one is an output by the LLM, then there should be a probability value which represent the probability of the LLM picking the third token given the first two tokens. In one word, this representative can be seen as a simulator of the base LLM when processing two tokens to generate the third one. 
    
    - How it can represent / contain a subset of the base LLM's knowledge? 
    
    - what is the efficacy of it?
  
  - The tri-gram matrix 
    
    - what is it?
    
    - how it work during the process?
    
    - why it can make such effect to benefit? 
  
  - Tree attention: 
    
    - Goal: verify the drafts
  
  - Self-improvement loop

- Creativity:
  
  - using a tri-gram matrix as the LLM representative

- Potential issue: 
  
  - (*question*) when it comes to long contexts, how can the representative guarantee the coherence if it only focus on the combination/style **given two get the third**?
    
    

### Third Iteration

#### Methodology:

- Current approaches: 
  
  - *Speculative decoding*
  
  - *Retrieval-based speculative decoding*
  
  - Algorithm: *Monte Carlo Tree Search (MCTS)*
  
  - 

- (*idea*) ADED = LLM Representative + Draft Maker

- (*idea*) Reusability seems going to be a big topic related to the efficiency improvement of LLM; create only once.
  
  

#### Ablation Study:

- Effect of MCTS:
  
  - *greedy search* and *full traversal* 
  
  - **Greedy Search**: this method picks the best (highest-probability) token at each step without considering other alternatives ----> a single, immediate best path  (over exploitation)
  
  - **Full Traversal / Comprehensive Exploration**: Explore all possible paths in the decision tree to determine the best overall sequence. However, because the search space in langauge generation is enormous, doing a full traversal is computationally infeasible. (over exploration)
  
  - MCTS is in the middle ground of above two methods
    
    
    
    
    
    
    
    
    
    
    
    

## Derived Paper Notes:

### LookAhead Decoding:

- Definition: a *guess and verify* mechanism
  
  - Utilzing jocobi algo to generate candidates, and new candidates generation will be influenced by last candidate. think about x_0 as given input, then first candidate will get [x_0^0, x_1^0, ..., x_w-1^0], and then the next candidate would be like [x_1^1, x_2^1, ... x_w^1] ... till candidate be like [x_N-1^2, x_N^2, ... x_N+W-2^2]. All these candidates will be stored in a pool. 
  
  - Select G candidates from the candidate pool with the lastest token of accepted generation, in this case, it is x_0. and the candidate would be a combination of token from different candidates at corresponding position, e.g., [x_1^0, x_2^1, x_3^2, ....]. then for all the conadidate, they will be fed to the base model in one batch. For each of the candidate, verify tokens **left-to-right** until a mistmatch: 
    
    - candidate: [x_4, x_5, x_6, ...]
    
    - P(x_4 | x_1, x_2, x_3) --> valid ?
    
    - P(x_5 | ..., x_4) --> valid? 
    
    - validity: argmax(P) = token_for_checking (greedy)
    
    - repeat utill first mismatch of the candidate
    
    - pick the candidate with longest accept length
    
    - append the candidate to the output to update the state
    
    - and now the new "latest token" is the last token in the picked candidate.
  
  - Hardcoding on CUDA and pytorch for a specifical implementation to adapt the algorithm. 
    
    
    
    

### REST: Retrieval-Based Speculative Decoding

- A method under the domain of "guess-and-verify" decoding, utilize a datastore to replace the function of the draft model in original speculative decoding. 
  
  - Datastore Construction: Based on a pre-built datastore
  
  - Retrieving from Datastore: Retrieve draft tokens from the datastore directly with a fast exact match method
  
  - Draft construction: 
    
    - Naive idea: sample a subset of sequences in S as the draft tokens: suboptimal due to randomness in sampling when S is large.
    
    - Final solution: Trie selection with frequency as weight.
  
  - Draft verification and acceptance: 
    
    - Pseudo sequence: "*each draft constitutes a sub-sequence of this pseudo sequence, and any shared prefix appears only once*" 
    
    - Attention mask: Tree Attention
    
    - Verification: feed the drafts to LLM, and sample new tokens from the conditional distribution at each position, then accept until first mistake.







### MEDUSA: Simple LLMInference Acceleration Framework with Multiple Decoding Heads


