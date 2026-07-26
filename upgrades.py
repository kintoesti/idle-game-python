"""
Système d'Upgrades
"""

from config import UPGRADES


class UpgradeSystem:
    """Gère les upgrades du jeu"""
    
    def __init__(self):
        self.upgrades = {}
        
        # Initialiser les upgrades
        for upgrade_id, upgrade_data in UPGRADES.items():
            self.upgrades[upgrade_id] = {
                "level": 0,
                "purchased": False
            }
    
    def buy_upgrade(self, upgrade_id, current_points):
        """Achète un upgrade"""
        if upgrade_id not in UPGRADES:
            return False, "Upgrade inexistant"
        
        upgrade = UPGRADES[upgrade_id]
        current_level = self.upgrades[upgrade_id]["level"]
        
        # Vérifier le niveau max
        if current_level >= upgrade.get("max_level", 1):
            return False, "Niveau maximum atteint"
        
        # Vérifier les points
        cost = upgrade["cost"] * (current_level + 1)  # Le coût augmente avec le niveau
        if current_points < cost:
            return False, f"Pas assez de points (besoin: {cost})"
        
        # Acheter l'upgrade
        self.upgrades[upgrade_id]["level"] += 1
        self.upgrades[upgrade_id]["purchased"] = True
        
        return True, cost
    
    def get_production_multiplier(self, generator_id):
        """Retourne le multiplicateur pour un générateur"""
        multiplier = 1.0
        
        for upgrade_id, upgrade_data in UPGRADES.items():
            if upgrade_data.get("target") == generator_id:
                upgrade_level = self.upgrades[upgrade_id]["level"]
                if upgrade_level > 0:
                    base_multiplier = upgrade_data.get("multiplier", 1.0)
                    multiplier *= base_multiplier ** upgrade_level
        
        return multiplier
    
    def get_upgrade_cost(self, upgrade_id):
        """Retourne le coût actuel d'un upgrade"""
        if upgrade_id not in UPGRADES:
            return 0
        
        upgrade = UPGRADES[upgrade_id]
        level = self.upgrades[upgrade_id]["level"]
        
        return upgrade["cost"] * (level + 1)
    
    def is_max_level(self, upgrade_id):
        """Vérifie si un upgrade est au niveau max"""
        if upgrade_id not in UPGRADES:
            return False
        
        upgrade = UPGRADES[upgrade_id]
        level = self.upgrades[upgrade_id]["level"]
        max_level = upgrade.get("max_level", 1)
        
        return level >= max_level
    
    def get_all_upgrades(self):
        """Retourne tous les upgrades"""
        return UPGRADES
    
    def to_dict(self):
        """Convertit en dictionnaire pour la sauvegarde"""
        return self.upgrades
    
    def from_dict(self, data):
        """Charge depuis un dictionnaire"""
        self.upgrades = data