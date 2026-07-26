"""
Idle Game - Un jeu inactif simple en Python
"""

import time
import json
import os
from datetime import datetime


class IdleGame:
    """Classe principale du jeu"""
    
    def __init__(self):
        self.points = 0
        self.generators = {
            "worker": {"cost": 10, "production": 1, "owned": 0},
            "factory": {"cost": 100, "production": 10, "owned": 0},
            "robot": {"cost": 1000, "production": 100, "owned": 0},
        }
        self.last_update = time.time()
        self.game_running = True
        self.save_file = "game_save.json"
        self.load_game()
    
    def display_ui(self):
        """Affiche l'interface du jeu"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 50)
        print("🍪 IDLE GAME 🍪".center(50))
        print("=" * 50)
        print(f"\n💰 Points: {self.points}\n")
        
        # Afficher la production par seconde
        production_per_sec = self.calculate_production_per_second()
        print(f"📈 Production/sec: +{production_per_sec}\n")
        
        # Afficher les générateurs
        print("--- GÉNÉRATEURS DISPONIBLES ---")
        for i, (name, data) in enumerate(self.generators.items(), 1):
            owned = data["owned"]
            cost = data["cost"]
            production = data["production"]
            print(f"{i}. {name.upper()}")
            print(f"   Coût: {cost} | Production: +{production}/sec | Possédés: {owned}")
            print()
        
        print("--- COMMANDES ---")
        print("1-3: Acheter un générateur")
        print("ESPACE: Cliquer (+1 point)")
        print("S: Sauvegarder")
        print("Q: Quitter")
        print("=" * 50)
    
    def click(self):
        """Le joueur clique"""
        self.points += 1
        print("✓ Clic! +1 point")
        time.sleep(0.3)
    
    def buy_generator(self, generator_name):
        """Achète un générateur"""
        if generator_name not in self.generators:
            print("❌ Générateur invalide!")
            return
        
        gen = self.generators[generator_name]
        cost = gen["cost"]
        
        if self.points >= cost:
            self.points -= cost
            gen["owned"] += 1
            print(f"✅ {generator_name} acheté! ({gen['owned']} possédé)")
        else:
            print(f"❌ Pas assez de points! (Besoin: {cost}, Tu as: {self.points})")
        
        time.sleep(0.5)
    
    def calculate_production_per_second(self):
        """Calcule la production par seconde"""
        total = 0
        for gen in self.generators.values():
            total += gen["owned"] * gen["production"]
        return total
    
    def update_production(self):
        """Met à jour les points basé sur les générateurs"""
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        production_per_sec = self.calculate_production_per_second()
        points_earned = production_per_sec * elapsed
        
        self.points += points_earned
        self.last_update = current_time
    
    def save_game(self):
        """Sauvegarde la progression"""
        data = {
            "points": self.points,
            "generators": self.generators,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.save_file, "w") as f:
            json.dump(data, f, indent=2)
        
        print("💾 Jeu sauvegardé!")
        time.sleep(0.5)
    
    def load_game(self):
        """Charge la progression sauvegardée"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.points = data.get("points", 0)
                    self.generators = data.get("generators", self.generators)
                    print("✅ Sauvegarde chargée!")
                    time.sleep(1)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement: {e}")
                time.sleep(1)
    
    def run(self):
        """Boucle principale du jeu"""
        try:
            import sys
            if sys.platform == "win32":
                import msvcrt
                get_key = lambda: msvcrt.getch().decode() if msvcrt.kbhit() else None
            else:
                import select
                def get_key():
                    if select.select([sys.stdin], [], [], 0)[0]:
                        return sys.stdin.read(1)
                    return None
        except:
            print("⚠️ Mode demo (pas de détection de touches)")
            get_key = lambda: None
        
        while self.game_running:
            self.update_production()
            self.display_ui()
            
            # Lecture de l'input (non-bloquante)
            key = get_key()
            
            if key:
                key = key.lower()
                if key == 'q':
                    self.save_game()
                    print("👋 À bientôt!")
                    self.game_running = False
                elif key == ' ':
                    self.click()
                elif key == 's':
                    self.save_game()
                elif key == '1':
                    self.buy_generator("worker")
                elif key == '2':
                    self.buy_generator("factory")
                elif key == '3':
                    self.buy_generator("robot")
            
            time.sleep(0.1)  # Petit délai pour ne pas surcharger CPU


def main():
    """Point d'entrée du jeu"""
    game = IdleGame()
    game.run()


if __name__ == "__main__":
    main()