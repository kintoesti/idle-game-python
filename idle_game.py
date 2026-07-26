"""
Idle Game - Version complète avec tous les systèmes
"""

import time
import json
import os
from datetime import datetime
from config import GENERATORS, UPGRADES, ACHIEVEMENTS, PRESTIGE_RESET_COST
from achievements import AchievementSystem
from upgrades import UpgradeSystem
from prestige import PrestigeSystem


class IdleGame:
    """Classe principale du jeu avec tous les systèmes"""
    
    def __init__(self):
        self.points = 0.0
        self.total_clicks = 0
        self.click_multiplier = 1.0
        self.production_multiplier = 1.0
        
        # Générateurs
        self.generators = {}
        for gen_id, gen_data in GENERATORS.items():
            self.generators[gen_id] = {
                "name": gen_data["name"],
                "cost": gen_data["cost"],
                "production": gen_data["production"],
                "icon": gen_data["icon"],
                "owned": 0,
                "multiplier": 1.0
            }
        
        # Systèmes
        self.achievement_system = AchievementSystem()
        self.upgrade_system = UpgradeSystem()
        self.prestige_system = PrestigeSystem()
        
        # Temps
        self.last_update = time.time()
        self.game_running = True
        self.save_file = "game_save.json"
        
        # UI
        self.current_menu = "main"
        self.new_achievements = []
        
        self.load_game()
    
    def display_header(self):
        """Affiche l'en-tête du jeu"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 70)
        print("🍪 IDLE GAME - VERSION COMPLÈTE 🍪".center(70))
        print("=" * 70)
    
    def display_stats(self):
        """Affiche les statistiques principales"""
        print(f"\n💰 Points: {int(self.points)}")
        print(f"📈 Production/sec: +{self.calculate_production_per_second():.0f}")
        print(f"🖱️  Clics: {self.total_clicks}")
        
        if self.prestige_system.prestige_level > 0:
            print(f"⭐ Prestige: Level {self.prestige_system.prestige_level} (+{self.prestige_system.get_production_bonus()*100:.0f}%)")
        
        unlocked_achievements = self.achievement_system.get_unlocked_count()
        total_achievements = len(ACHIEVEMENTS)
        print(f"🏆 Achievements: {unlocked_achievements}/{total_achievements}")
        print()
    
    def display_main_menu(self):
        """Affiche le menu principal"""
        self.display_header()
        self.display_stats()
        
        print("--- ACTIONS ---")
        print("ESPACE: Cliquer (+1 point)")
        print("1-4: Acheter un générateur")
        print("U: Upgrades")
        print("A: Achievements")
        print("P: Prestige")
        print("S: Sauvegarder")
        print("Q: Quitter")
        print("=" * 70)
    
    def display_generators(self):
        """Affiche les générateurs disponibles"""
        self.display_header()
        self.display_stats()
        
        print("--- GÉNÉRATEURS DISPONIBLES ---\n")
        
        gen_list = list(self.generators.items())
        for i, (gen_id, gen_data) in enumerate(gen_list, 1):
            owned = gen_data["owned"]
            cost = gen_data["cost"]
            production = gen_data["production"]
            icon = gen_data["icon"]
            multiplier = self.upgrade_system.get_production_multiplier(gen_id)
            actual_production = production * multiplier
            
            print(f"{i}. {icon} {gen_data['name'].upper()}")
            print(f"   Coût: {cost:,} | Production: +{actual_production:.0f}/sec | Possédés: {owned}")
            if multiplier > 1.0:
                print(f"   ⚡ Multiplicateur: x{multiplier:.1f}")
            print()
    
    def display_upgrades(self):
        """Affiche les upgrades disponibles"""
        self.display_header()
        self.display_stats()
        
        print("--- UPGRADES DISPONIBLES ---\n")
        
        for i, (upgrade_id, upgrade_data) in enumerate(UPGRADES.items(), 1):
            level = self.upgrade_system.upgrades[upgrade_id]["level"]
            max_level = upgrade_data.get("max_level", 1)
            cost = self.upgrade_system.get_upgrade_cost(upgrade_id)
            is_max = self.upgrade_system.is_max_level(upgrade_id)
            
            status = "✅ MAX" if is_max else f"Niveau: {level}/{max_level}"
            print(f"{i}. {upgrade_data['name']}")
            print(f"   {upgrade_data['description']}")
            print(f"   Coût: {cost:,} | {status}")
            print()
    
    def display_achievements(self):
        """Affiche les achievements"""
        self.display_header()
        self.display_stats()
        
        print("--- ACHIEVEMENTS ---\n")
        
        for achievement_id, achievement_data in ACHIEVEMENTS.items():
            is_unlocked = self.achievement_system.is_unlocked(achievement_id)
            icon = "✅" if is_unlocked else "🔒"
            
            print(f"{icon} {achievement_data['icon']} {achievement_data['name']}")
            print(f"   {achievement_data['description']}")
            if is_unlocked:
                print(f"   💎 Récompense: +{achievement_data['points']} points")
            print()
    
    def display_prestige(self):
        """Affiche le menu prestige"""
        self.display_header()
        self.display_stats()
        
        prestige_points = self.prestige_system.calculate_prestige_points(self.points)
        can_prestige = self.prestige_system.can_prestige(self.points)
        
        print("--- PRESTIGE ---\n")
        print(f"Prestige Level: {self.prestige_system.prestige_level}")
        print(f"Production Bonus: +{self.prestige_system.get_production_bonus()*100:.0f}%")
        print(f"Total Prestige Points: {self.prestige_system.total_prestige_points}\n")
        
        print(f"Points nécessaires pour prestige: {PRESTIGE_RESET_COST:,}")
        print(f"Points que tu gagneras: {prestige_points}")
        
        if can_prestige:
            print("\n⚠️  Le prestige réinitialisera tous tes générateurs!")
            print("Confirmer? (Y/N)")
        else:
            print(f"\n❌ Pas assez de points (manque: {PRESTIGE_RESET_COST - int(self.points):,})")
    
    def click(self):
        """Le joueur clique"""
        click_value = 1.0 * self.click_multiplier * self.prestige_system.get_click_bonus()
        self.points += click_value
        self.total_clicks += 1
        print(f"✓ Clic! +{click_value:.1f} point")
        time.sleep(0.2)
    
    def buy_generator(self, generator_id):
        """Achète un générateur"""
        if generator_id not in self.generators:
            print("❌ Générateur invalide!")
            return
        
        gen = self.generators[generator_id]
        cost = gen["cost"]
        
        if self.points >= cost:
            self.points -= cost
            gen["owned"] += 1
            print(f"✅ {gen['name']} acheté! ({gen['owned']} possédé)")
        else:
            print(f"❌ Pas assez de points! (Besoin: {cost:,}, Tu as: {int(self.points)})")
        
        time.sleep(0.5)
    
    def buy_upgrade(self, upgrade_id):
        """Achète un upgrade"""
        success, message = self.upgrade_system.buy_upgrade(upgrade_id, self.points)
        
        if success:
            self.points -= message  # message contient le coût
            print(f"✅ Upgrade acheté!")
        else:
            print(f"❌ {message}")
        
        time.sleep(0.5)
    
    def calculate_production_per_second(self):
        """Calcule la production par seconde"""
        total = 0
        for gen_id, gen in self.generators.items():
            multiplier = self.upgrade_system.get_production_multiplier(gen_id)
            production = gen["owned"] * gen["production"] * multiplier
            total += production
        
        # Appliquer le multiplicateur de prestige
        prestige_bonus = 1.0 + self.prestige_system.get_production_bonus()
        total *= prestige_bonus
        total *= self.production_multiplier
        
        return total
    
    def update_production(self):
        """Met à jour les points basé sur les générateurs"""
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        production_per_sec = self.calculate_production_per_second()
        points_earned = production_per_sec * elapsed
        
        self.points += points_earned
        self.last_update = current_time
    
    def check_achievements(self):
        """Vérifie les achievements"""
        game_state = {
            "points": int(self.points),
            "total_clicks": self.total_clicks,
            "generators": self.generators,
            "prestige_level": self.prestige_system.prestige_level
        }
        
        newly_unlocked = self.achievement_system.check_achievements(game_state)
        
        if newly_unlocked:
            self.new_achievements = newly_unlocked
            for achievement_id in newly_unlocked:
                reward = self.achievement_system.get_reward(achievement_id)
                self.points += reward
    
    def prestige(self):
        """Effectue un prestige"""
        success, prestige_points = self.prestige_system.prestige(self.points)
        
        if success:
            print(f"✨ Prestige effectué! +{prestige_points} prestige points")
            self.points = 0
            
            # Réinitialiser les générateurs
            for gen in self.generators.values():
                gen["owned"] = 0
            
            # Réinitialiser les upgrades
            self.upgrade_system = UpgradeSystem()
        else:
            print(f"❌ {prestige_points}")
        
        time.sleep(1)
    
    def save_game(self):
        """Sauvegarde la progression"""
        data = {
            "points": self.points,
            "total_clicks": self.total_clicks,
            "generators": self.generators,
            "upgrades": self.upgrade_system.to_dict(),
            "achievements": self.achievement_system.to_dict(),
            "prestige": self.prestige_system.to_dict(),
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
                    self.total_clicks = data.get("total_clicks", 0)
                    self.generators = data.get("generators", self.generators)
                    self.upgrade_system.from_dict(data.get("upgrades", {}))
                    self.achievement_system.from_dict(data.get("achievements", {}))
                    self.prestige_system.from_dict(data.get("prestige", {}))
                    print("✅ Sauvegarde chargée!")
                    time.sleep(1)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement: {e}")
                time.sleep(1)
    
    def run(self):
        """Boucle principale du jeu"""
        while self.game_running:
            self.update_production()
            self.check_achievements()
            
            if self.current_menu == "main":
                self.display_main_menu()
            elif self.current_menu == "generators":
                self.display_generators()
            elif self.current_menu == "upgrades":
                self.display_upgrades()
            elif self.current_menu == "achievements":
                self.display_achievements()
            elif self.current_menu == "prestige":
                self.display_prestige()
            
            # Afficher les nouveaux achievements
            if self.new_achievements:
                for achievement_id in self.new_achievements:
                    achievement = ACHIEVEMENTS[achievement_id]
                    print(f"\n🎉 ACHIEVEMENT DÉBLOQUÉ: {achievement['icon']} {achievement['name']}!")
                self.new_achievements = []
                time.sleep(1)
            
            # Lire l'input
            try:
                key = input("\n> ").lower()
            except:
                key = ""
            
            if key == 'q':
                self.save_game()
                print("👋 À bientôt!")
                self.game_running = False
            elif key == ' ' or key == '':
                if self.current_menu == "main":
                    self.click()
                    self.current_menu = "main"
            elif key == 's':
                self.save_game()
                self.current_menu = "main"
            elif key == '1' and self.current_menu == "main":
                self.buy_generator("worker")
                self.current_menu = "main"
            elif key == '2' and self.current_menu == "main":
                self.buy_generator("factory")
                self.current_menu = "main"
            elif key == '3' and self.current_menu == "main":
                self.buy_generator("robot")
                self.current_menu = "main"
            elif key == '4' and self.current_menu == "main":
                self.buy_generator("ai")
                self.current_menu = "main"
            elif key == 'u' and self.current_menu == "main":
                self.current_menu = "upgrades"
            elif key in ['1', '2', '3'] and self.current_menu == "upgrades":
                upgrade_ids = list(UPGRADES.keys())
                if int(key) - 1 < len(upgrade_ids):
                    self.buy_upgrade(upgrade_ids[int(key) - 1])
                self.current_menu = "upgrades"
            elif key == 'a' and self.current_menu == "main":
                self.current_menu = "achievements"
            elif key == 'p' and self.current_menu == "main":
                self.current_menu = "prestige"
            elif key == 'y' and self.current_menu == "prestige":
                self.prestige()
                self.current_menu = "main"
            elif key == 'n' and self.current_menu == "prestige":
                self.current_menu = "main"
            elif key == 'm':
                self.current_menu = "main"


def main():
    """Point d'entrée du jeu"""
    game = IdleGame()
    game.run()


if __name__ == "__main__":
    main()
