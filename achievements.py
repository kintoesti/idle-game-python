"""
Système d'Achievements (Succès)
"""

from config import ACHIEVEMENTS


class AchievementSystem:
    """Gère les succès du jeu"""
    
    def __init__(self):
        self.unlocked = {}  # {achievement_id: unlock_time}
        self.progress = {}  # Suivi des progrès partiels
        
        # Initialiser les achievements
        for achievement_id in ACHIEVEMENTS:
            self.unlocked[achievement_id] = None
            self.progress[achievement_id] = 0
    
    def unlock(self, achievement_id):
        """Déverrouille un succès"""
        if achievement_id not in ACHIEVEMENTS:
            return False
        
        if self.unlocked[achievement_id] is not None:
            return False  # Déjà déverrouillé
        
        self.unlocked[achievement_id] = True
        return True
    
    def is_unlocked(self, achievement_id):
        """Vérifie si un succès est déverrouillé"""
        return self.unlocked.get(achievement_id) is not None
    
    def get_reward(self, achievement_id):
        """Retourne la récompense d'un succès"""
        if achievement_id in ACHIEVEMENTS:
            return ACHIEVEMENTS[achievement_id].get("points", 0)
        return 0
    
    def check_achievements(self, game_state):
        """Vérifie et déverrouille les achievements possibles"""
        newly_unlocked = []
        
        # First Click
        if game_state["total_clicks"] >= 1 and not self.is_unlocked("first_click"):
            newly_unlocked.append("first_click")
            self.unlock("first_click")
        
        # Thousand Points
        if game_state["points"] >= 1000 and not self.is_unlocked("thousand_points"):
            newly_unlocked.append("thousand_points")
            self.unlock("thousand_points")
        
        # First Worker
        if game_state["generators"]["worker"]["owned"] >= 1 and not self.is_unlocked("first_worker"):
            newly_unlocked.append("first_worker")
            self.unlock("first_worker")
        
        # Ten Workers
        if game_state["generators"]["worker"]["owned"] >= 10 and not self.is_unlocked("ten_workers"):
            newly_unlocked.append("ten_workers")
            self.unlock("ten_workers")
        
        # Factory Owner
        if game_state["generators"]["factory"]["owned"] >= 1 and not self.is_unlocked("factory_owner"):
            newly_unlocked.append("factory_owner")
            self.unlock("factory_owner")
        
        # Robot Master
        if game_state["generators"]["robot"]["owned"] >= 1 and not self.is_unlocked("robot_master"):
            newly_unlocked.append("robot_master")
            self.unlock("robot_master")
        
        # Million Points
        if game_state["points"] >= 1000000 and not self.is_unlocked("million_points"):
            newly_unlocked.append("million_points")
            self.unlock("million_points")
        
        # Prestige Achievement
        if game_state["prestige_level"] >= 1 and not self.is_unlocked("prestige_1"):
            newly_unlocked.append("prestige_1")
            self.unlock("prestige_1")
        
        return newly_unlocked
    
    def get_all_achievements(self):
        """Retourne tous les achievements"""
        return ACHIEVEMENTS
    
    def get_unlocked_count(self):
        """Retourne le nombre de succès déverrouillés"""
        return sum(1 for unlocked in self.unlocked.values() if unlocked is not None)
    
    def to_dict(self):
        """Convertit en dictionnaire pour la sauvegarde"""
        return {
            "unlocked": self.unlocked,
            "progress": self.progress
        }
    
    def from_dict(self, data):
        """Charge depuis un dictionnaire"""
        self.unlocked = data.get("unlocked", self.unlocked)
        self.progress = data.get("progress", self.progress)