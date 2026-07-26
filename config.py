"""
Configuration et constantes du jeu
"""

# === GÉNÉRATEURS ===
GENERATORS = {
    "worker": {
        "name": "Ouvrier",
        "cost": 10,
        "production": 1,
        "icon": "👷"
    },
    "factory": {
        "name": "Usine",
        "cost": 100,
        "production": 10,
        "icon": "🏭"
    },
    "robot": {
        "name": "Robot",
        "cost": 1000,
        "production": 100,
        "icon": "🤖"
    },
    "ai": {
        "name": "IA",
        "cost": 10000,
        "production": 1000,
        "icon": "🧠"
    }
}

# === UPGRADES ===
UPGRADES = {
    "double_worker": {
        "name": "Ouvriers x2",
        "cost": 100,
        "description": "Les ouvriers produisent 2x plus",
        "target": "worker",
        "multiplier": 2.0,
        "max_level": 5
    },
    "factory_boost": {
        "name": "Turbo Usine",
        "cost": 500,
        "description": "Les usines produisent 2x plus",
        "target": "factory",
        "multiplier": 2.0,
        "max_level": 5
    },
    "robot_upgrade": {
        "name": "Amélioration Robot",
        "cost": 5000,
        "description": "Les robots produisent 2x plus",
        "target": "robot",
        "multiplier": 2.0,
        "max_level": 5
    }
}

# === ACHIEVEMENTS ===
ACHIEVEMENTS = {
    "first_click": {
        "name": "Premier Clic",
        "description": "Fais ton premier clic",
        "icon": "🖱️",
        "points": 10
    },
    "thousand_points": {
        "name": "Mille Points",
        "description": "Atteins 1000 points",
        "icon": "💰",
        "points": 50
    },
    "first_worker": {
        "name": "Employeur",
        "description": "Achète ton premier ouvrier",
        "icon": "👷",
        "points": 25
    },
    "ten_workers": {
        "name": "Empire Ouvrier",
        "description": "Possède 10 ouvriers",
        "icon": "👥",
        "points": 100
    },
    "factory_owner": {
        "name": "Propriétaire d'Usine",
        "description": "Achète ta première usine",
        "icon": "🏭",
        "points": 50
    },
    "robot_master": {
        "name": "Maître Robot",
        "description": "Achète ton premier robot",
        "icon": "🤖",
        "points": 200
    },
    "million_points": {
        "name": "Millionnaire",
        "description": "Atteins 1 million de points",
        "icon": "💎",
        "points": 500
    },
    "prestige_1": {
        "name": "Prestige I",
        "description": "Effectue ton premier prestige",
        "icon": "⭐",
        "points": 1000
    }
}

# === MULTIPLICATEURS ===
MULTIPLIERS = {
    "click_multiplier": 1.0,      # Multiplicateur de clic
    "production_multiplier": 1.0  # Multiplicateur de production globale
}

# === PRESTIGE ===
PRESTIGE_RESET_COST = 1000000  # Points nécessaires pour prestige
PRESTIGE_BONUS_PER_LEVEL = 0.01  # +1% production par niveau de prestige