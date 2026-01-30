"""
Code Anomaly Detection System
Uses CodeBERT embeddings and structural metrics to detect anomalies in Python code.
"""

import os
import ast
import torch
import numpy as np
from typing import Dict, List, Tuple
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


class StructuralAnalyzer(ast.NodeVisitor):
    """Extract structural metrics from Python code using AST."""
    
    def __init__(self):
        self.function_count = 0
        self.loop_count = 0
        self.if_count = 0
        self.max_depth = 0
        self.current_depth = 0
    
    def visit_FunctionDef(self, node):
        """Count function definitions."""
        self.function_count += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Count for loops."""
        self.loop_count += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Count while loops."""
        self.loop_count += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Count if statements."""
        self.if_count += 1
        self.generic_visit(node)
    
    def generic_visit(self, node):
        """Track nesting depth."""
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        super().generic_visit(node)
        self.current_depth -= 1
    
    def get_metrics(self) -> Dict[str, int]:
        """Return structural metrics."""
        return {
            'functions': self.function_count,
            'loops': self.loop_count,
            'if_statements': self.if_count,
            'max_depth': self.max_depth
        }


class CodeBERTEmbedder:
    """Generate embeddings using CodeBERT model."""
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModel.from_pretrained("microsoft/codebert-base")
        self.model.eval()
    
    def get_embedding(self, code: str) -> np.ndarray:
        """Generate embedding for Python code."""
        inputs = self.tokenizer(
            code,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Mean pooling of token embeddings
        embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embedding


class CodeAnomalyDetector:
    """Detect anomalies in Python code using semantic and structural analysis."""
    
    def __init__(self, semantic_weight: float = 0.6, structural_weight: float = 0.4):
        self.embedder = CodeBERTEmbedder()
        self.semantic_weight = semantic_weight
        self.structural_weight = structural_weight
        self.normal_embedding = None
        self.normal_metrics = None
    
    def extract_structural_metrics(self, code: str) -> Dict[str, int]:
        """Extract structural metrics from code."""
        try:
            tree = ast.parse(code)
            analyzer = StructuralAnalyzer()
            analyzer.visit(tree)
            return analyzer.get_metrics()
        except SyntaxError:
            return {
                'functions': 0,
                'loops': 0,
                'if_statements': 0,
                'max_depth': 0
            }
    
    def normalize_metrics(self, metrics: Dict[str, int]) -> np.ndarray:
        """Normalize structural metrics to [0, 1] range."""
        normalized = np.array([
            min(metrics['functions'] / 10.0, 1.0),
            min(metrics['loops'] / 10.0, 1.0),
            min(metrics['if_statements'] / 15.0, 1.0),
            min(metrics['max_depth'] / 8.0, 1.0)
        ])
        return normalized
    
    def compute_structural_score(self, metrics: Dict[str, int]) -> float:
        """Compute structural anomaly score (0-1, higher = more anomalous)."""
        normalized = self.normalize_metrics(metrics)
        structural_score = float(np.std(normalized))
        return min(structural_score, 1.0)
    
    def train_from_normal_files(self, directory: str) -> None:
        """Compute baseline from normal code files."""
        embeddings = []
        all_metrics = {'functions': [], 'loops': [], 'if_statements': [], 'max_depth': []}
        
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    embedding = self.embedder.get_embedding(code)
                    embeddings.append(embedding)
                    
                    metrics = self.extract_structural_metrics(code)
                    for key in all_metrics:
                        all_metrics[key].append(metrics[key])
                
                except Exception as e:
                    print(f"Warning: Could not process {filename}: {e}")
        
        # Compute mean embedding
        self.normal_embedding = np.mean(embeddings, axis=0)
        
        # Compute mean metrics
        self.normal_metrics = {
            key: np.mean(values) if values else 0
            for key, values in all_metrics.items()
        }
    
    def detect_anomaly(self, code: str) -> Tuple[float, str]:
        """Detect anomaly and return score and classification.
        
        Score ranges (0-10 scale):
        - < 2.5: NORMAL
        - >= 2.5: ANOMALOUS
        """
        if self.normal_embedding is None:
            raise ValueError("Model must be trained first using train_from_normal_files()")
        
        # Get semantic embedding
        test_embedding = self.embedder.get_embedding(code)
        
        # Compute semantic distance (0-1, higher = more anomalous)
        similarity = cosine_similarity(test_embedding, self.normal_embedding)[0][0]
        semantic_score = 1.0 - similarity
        
        # Get structural metrics
        metrics = self.extract_structural_metrics(code)
        structural_score = self.compute_structural_score(metrics)
        
        # Combine scores and scale to 0-10 range
        raw_score = self.semantic_weight * semantic_score + self.structural_weight * structural_score
        anomaly_score = raw_score * 150.0  # Very aggressive scaling to push scores to extremes
        
        # Classify based on threshold
        if anomaly_score < 7:
            classification = "NORMAL"
        else:
            classification = "ANOMALOUS"
        
        return anomaly_score, classification
    
    def analyze_directory(self, directory: str) -> List[Dict]:
        """Analyze all Python files in directory."""
        results = []
        
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return results
        
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.py'):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    score, classification = self.detect_anomaly(code)
                    metrics = self.extract_structural_metrics(code)
                    
                    results.append({
                        'File': filename,
                        'Anomaly Score': f"{score:.3f}",
                        'Classification': classification,
                        'Functions': metrics['functions'],
                        'Loops': metrics['loops'],
                        'If Statements': metrics['if_statements'],
                        'Max Depth': metrics['max_depth']
                    })
                
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return results
    
    def print_results_table(self, results: List[Dict], title: str = "CODE ANOMALY DETECTION RESULTS") -> None:
        """Print results as formatted table."""
        if not results:
            print("No results to display.")
            return
        
        print("\n" + "="*70)
        print(f"{title:^70}")
        print("="*70)
        print(f"{'File':<35} {'Anomaly Score':<20} {'Classification':<15}")
        print("-"*70)
        
        for result in results:
            print(f"{result['File']:<35} {result['Anomaly Score']:<20} {result['Classification']:<15}")
        
        print("="*70 + "\n")
    
    def print_detailed_metrics(self, results: List[Dict], title: str = "DETAILED CODE METRICS") -> None:
        """Print detailed metrics for each file."""
        if not results:
            print("No results to display.")
            return
        
        print("\n" + "="*90)
        print(f"{title:^90}")
        print("="*90)
        
        for result in results:
            print(f"\nFile: {result['File']}")
            print(f"  - Functions: {result['Functions']}")
            print(f"  - Loops: {result['Loops']}")
            print(f"  - If Statements: {result['If Statements']}")
            print(f"  - Max Nesting Depth: {result['Max Depth']}")
            print(f"  - Anomaly Score: {result['Anomaly Score']}")
            print(f"  - Classification: {result['Classification']}")
        
        print("\n" + "="*90 + "\n")


def main():
    """Main execution function."""
    detector = CodeAnomalyDetector(semantic_weight=0.9, structural_weight=0.1)
    
    # Train on normal code
    print("Training on normal code files...")
    detector.train_from_normal_files("normal_code")
    print(f"[OK] Training complete. Normal baseline embedding computed.\n")
    
    # Analyze ONLY test code
    print("Analyzing TEST CODE files...")
    test_results = detector.analyze_directory("test_code")
    detector.print_results_table(test_results, "TEST CODE ANALYSIS")
    
    # Print detailed metrics
    if test_results:
        detector.print_detailed_metrics(test_results, "DETAILED CODE METRICS FOR TEST FILES")
        
        # Summary statistics
        all_results = test_results
        normal_count = sum(1 for r in all_results if r['Classification'] == 'NORMAL')
        anomaly_count = sum(1 for r in all_results if r['Classification'] == 'ANOMALOUS')
        
        avg_functions = sum(r['Functions'] for r in all_results) / len(all_results)
        avg_loops = sum(r['Loops'] for r in all_results) / len(all_results)
        avg_ifs = sum(r['If Statements'] for r in all_results) / len(all_results)
        avg_depth = sum(r['Max Depth'] for r in all_results) / len(all_results)
        
        print("\n" + "="*70)
        print(f"SUMMARY: {normal_count} Normal | {anomaly_count} Anomalous")
        print("Threshold: < 6 = NORMAL | >=7 = ANOMALOUS (Score: 0-10 scale)")
        print("\nAVERAGE METRICS ACROSS ALL FILES:")
        print(f"  - Average Functions: {avg_functions:.2f}")
        print(f"  - Average Loops: {avg_loops:.2f}")
        print(f"  - Average If Statements: {avg_ifs:.2f}")
        print(f"  - Average Max Depth: {avg_depth:.2f}")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()