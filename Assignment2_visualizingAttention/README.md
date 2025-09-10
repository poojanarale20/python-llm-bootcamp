"# visualize-bert-attention" 


Project Overview
This notebook demonstrates how to:
Load a pre-trained BERT model
Process text through the model
Extract and visualize attention weights to understand how the model "focuses" on different parts of the input


Cell 1: Imports
transformers: Hugging Face's library for working with pre-trained transformer models
BertTokenizer: Converts text into tokens that BERT can understand
BertModel: The actual BERT model architecture
bertviz: A visualization library specifically for transformer attention
torch: PyTorch for tensor operations

Cell 2: Model Loading

Loads the bert-base-uncased model (12-layer, 768-hidden, 12-heads, 110M parameters)
output_attentions=True is crucial - this tells the model to return attention weights
The tokenizer converts text into the format BERT expects

Cell 3: Text Processing
Takes the sentence "Transformers are amazing!"
Tokenizes it (breaks into subwords like "Transform", "##ers", "are", "amazing", "!")
Converts to PyTorch tensors (return_tensors="pt")
Gets the actual token strings for visualization


Cell 4: Model Inference
Runs the sentence through BERT
torch.no_grad() disables gradient calculation (faster, less memory)
Extracts attention weights from all 12 layers

Cell 5: Shape Analysis
Shows the dimensions of various outputs
Helps understand the model's internal structure

Cell 6: Visualization
Creates an interactive visualization showing attention patterns
You can see which words the model "attends to" when processing each token
Shows attention across all 12 layers and 12 attention heads

What You'll See
The visualization will show:
Layers: 12 different layers (each building on the previous)
Heads: 12 attention heads per layer (each focusing on different relationships)
Attention patterns: Lines connecting tokens, with thickness indicating attention strength
Interactive exploration: You can click on different layers/heads to see different attention patterns
Key Concepts
Attention: How much each word "pays attention" to other words
Multi-head attention: Different heads focus on different types of relationships (syntax, semantics, etc.)
Layer depth: Deeper layers capture more complex, abstract relationships
This is a powerful tool for understanding how transformer models like BERT process language and build representations of meaning!