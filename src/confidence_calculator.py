import numpy as np
import yaml

class ConfidenceCalculator:
    """
    Calculate confidence scores using Z-score normalization and tunable weights.
    
    This class generates confidence scores based on multiple independent criteria,
    normalizes them using Z-score normalization, and combines them using
    configurable weights.
    """
    
    def __init__(self, config_path="config/confidence_weights.yaml"):
        """
        Initialize the confidence calculator with weights from configuration.
        
        Args:
            config_path: Path to the configuration file with weights
        """
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
                self.weights = self.config.get("weights", {
                    "semantic_similarity": 0.4,
                    "relation_consistency": 0.3,
                    "data_completeness": 0.3
                })
        except FileNotFoundError:
            # Default weights if configuration file is not found
            self.weights = {
                "semantic_similarity": 0.4,
                "relation_consistency": 0.3,
                "data_completeness": 0.3
            }
    
    def z_score_normalize(self, scores):
        """
        Normalize scores using Z-score normalization.
        
        Args:
            scores: NumPy array of scores to normalize
            
        Returns:
            Normalized scores as a NumPy array
        """
        if len(scores) <= 1:
            return np.zeros_like(scores)
            
        mean = np.mean(scores)
        std = np.std(scores)
        
        # Avoid division by zero
        if std == 0:
            return np.zeros_like(scores)
            
        return (scores - mean) / std
    
    def calculate_scores(self, triples):
        """
        Calculate confidence scores for a list of triples.
        
        Args:
            triples: List of triple dictionaries with s, p, o keys
            
        Returns:
            List of triples with updated confidence scores
        """
        if not triples:
            return triples
            
        # Extract features for all triples
        semantic_scores = self._calculate_semantic_scores(triples)
        consistency_scores = self._calculate_consistency_scores(triples)
        completeness_scores = self._calculate_completeness_scores(triples)
        
        # Normalize scores
        normalized_semantic = self.z_score_normalize(semantic_scores)
        normalized_consistency = self.z_score_normalize(consistency_scores)
        normalized_completeness = self.z_score_normalize(completeness_scores)
        
        # Combine scores with weights
        weighted_scores = (
            self.weights["semantic_similarity"] * normalized_semantic +
            self.weights["relation_consistency"] * normalized_consistency +
            self.weights["data_completeness"] * normalized_completeness
        )
        
        # Convert to percentile range (0-1)
        min_score = np.min(weighted_scores)
        max_score = np.max(weighted_scores)
        
        if min_score == max_score:
            # If all scores are the same, assign middle confidence
            confidence_scores = np.full_like(weighted_scores, 0.5)
        else:
            # Scale to range [0.1, 1.0] to avoid extremely low confidence
            confidence_scores = 0.1 + 0.9 * (weighted_scores - min_score) / (max_score - min_score)
        
        # Update triples with new confidence scores
        for i, triple in enumerate(triples):
            triple["confidence"] = float(confidence_scores[i])
            
        return triples
    
    def _calculate_semantic_scores(self, triples):
        """
        Calculate semantic similarity scores for triples.
        
        In a real implementation, this would evaluate how semantically
        meaningful a triple is. For now, we use a heuristic based on
        existing confidence if available.
        
        Args:
            triples: List of triple dictionaries
            
        Returns:
            NumPy array of semantic scores
        """
        scores = []
        for triple in triples:
            # Use existing confidence as a base if available, otherwise 0.7
            base_score = float(triple.get("confidence", 0.7))
            
            # Adjust score based on predicate and object types
            # More sophisticated implementations would use language models
            p = triple["p"]
            o = triple["o"]
            
            score_adjustment = 0.0
            
            # Check if object looks like a date for date-related predicates
            if "date" in p.lower() or "birth" in p.lower():
                if "-" in o and len(o) >= 8:  # Looks like a date format
                    score_adjustment += 0.2
            
            # Check for location predicates
            if "place" in p.lower() or "location" in p.lower():
                if o[0].isupper():  # Location names typically start with uppercase
                    score_adjustment += 0.1
            
            scores.append(base_score + score_adjustment)
        
        return np.array(scores)
    
    def _calculate_consistency_scores(self, triples):
        """
        Calculate consistency scores based on how well a triple
        conforms to expected patterns for its predicate type.
        
        Args:
            triples: List of triple dictionaries
            
        Returns:
            NumPy array of consistency scores
        """
        scores = []
        
        # Group triples by subject and predicate
        grouped = {}
        for i, triple in enumerate(triples):
            key = (triple["s"], triple["p"])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(i)
        
        for i, triple in enumerate(triples):
            # Base score
            score = 0.7
            
            # Functional predicates should be unique
            key = (triple["s"], triple["p"])
            if len(grouped[key]) > 1:
                # Predicates that should be functional have consistency penalties
                if "id" in triple["p"].lower() or "date" in triple["p"].lower():
                    score -= 0.3
            
            # Type consistency
            p = triple["p"]
            o = triple["o"]
            
            # Date fields should look like dates
            if "date" in p.lower():
                if "-" in o and (len(o) == 10 or len(o) == 7):  # YYYY-MM-DD or YYYY-MM
                    score += 0.2
                elif o.isdigit() and len(o) == 4:  # YYYY
                    score += 0.1
                else:
                    score -= 0.2
            
            # Location fields should be proper nouns
            if "place" in p.lower() or "location" in p.lower():
                if o[0].isupper() and o.isalpha():
                    score += 0.2
                elif o[0].isupper():
                    score += 0.1
            
            scores.append(score)
        
        return np.array(scores)
    
    def _calculate_completeness_scores(self, triples):
        """
        Calculate completeness scores based on how complete the information is.
        
        Args:
            triples: List of triple dictionaries
            
        Returns:
            NumPy array of completeness scores
        """
        scores = []
        
        for triple in triples:
            # Base score
            score = 0.7
            
            # Check for empty or minimal values
            o = triple["o"]
            if not o:
                score = 0.1
            elif len(o) < 2:
                score = 0.3
            elif len(o) > 3:
                score += 0.1
            
            # Bonus for well-formatted data
            if "date" in triple["p"].lower():
                if len(o.split("-")) == 3:  # Complete date
                    score += 0.2
            
            scores.append(score)
        
        return np.array(scores)
