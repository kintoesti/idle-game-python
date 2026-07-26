"""
Système de Prestige (redémarrer avec bonus)
"""

from config import PRESTIGE_RESET_COST, PRESTIGE_BONUS_PER_LEVEL


class PrestigeSystem:
    """Gère le système de prestige"""
    
    def __init__(self):
        self.prestige_level = 0
        self.prestige_points = 0
        self.total_prestige_points = 0
    
    def calculate_prestige_points(self, current_points):
        """Calcule les points de prestige gagnés"""
        # Formule simple : racine carré du nombre de points divisée par 1000
        prestige = int((current_points ** 0.5) / 10)
        return prestige
    
    def can_prestige(self, current_points):
        """Vérifie si on peut faire un prestige"""
        return current_points >= PRESTIGE_RESET_COST
    
    def prestige(self, current_points):
        """Effectue un prestige"""
        if not self.can_prestige(current_points):
            return False, "Pas assez de points"
        
        new_prestige_points = self.calculate_prestige_points(current_points)
        
        self.prestige_level += 1
        self.prestige_points += new_prestige_points
        self.total_prestige_points += new_prestige_points
        
        return True, new_prestige_points
    
    def get_production_bonus(self):
        """Retourne le bonus de production du prestige (en %)"""
        return self.prestige_level * PRESTIGE_BONUS_PER_LEVEL
    
    def get_click_bonus(self):
        """Retourne le bonus de clic du prestige"""
        return 1.0 + (self.prestige_level * PRESTIGE_BONUS_PER_LEVEL)
    
    def to_dict(self):
        """Convertit en dictionnaire pour la sauvegarde"""
        return {
            "prestige_level": self.prestige_level,
            "prestige_points": self.prestige_points,
            "total_prestige_points": self.total_prestige_points
        }
    
    def from_dict(self, data):
        """Charge depuis un dictionnaire"""
        self.prestige_level = data.get("prestige_level", 0)
        self.prestige_points = data.get("prestige_points", 0)
        self.total_prestige_points = data.get("total_prestige_points", 0)
