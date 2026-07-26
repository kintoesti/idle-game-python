"""
Idle Game GUI - Version graphique avec Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from config import GENERATORS, UPGRADES, ACHIEVEMENTS, PRESTIGE_RESET_COST
from achievements import AchievementSystem
from upgrades import UpgradeSystem
from prestige import PrestigeSystem


class IdleGameGUI:
    """Interface graphique du jeu avec Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🍪 Idle Game - Python Edition")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Initialiser le jeu
        self.points = 0.0
        self.total_clicks = 0
        self.generators = {}
        self.achievement_system = AchievementSystem()
        self.upgrade_system = UpgradeSystem()
        self.prestige_system = PrestigeSystem()
        self.save_file = "game_save.json"
        self.last_update_time = datetime.now()
        
        for gen_id, gen_data in GENERATORS.items():
            self.generators[gen_id] = {
                "name": gen_data["name"],
                "cost": gen_data["cost"],
                "production": gen_data["production"],
                "icon": gen_data["icon"],
                "owned": 0,
            }
        
        self.load_game()
        self.create_ui()
        self.update_game()
    
    def create_ui(self):
        """Crée l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === HEADER ===
        header = ttk.Label(main_frame, text="🍪 IDLE GAME 🍪", font=("Arial", 24, "bold"))
        header.grid(row=0, column=0, columnspan=3, pady=10)
        
        # === STATS ===
        stats_frame = ttk.LabelFrame(main_frame, text="📊 STATISTIQUES", padding="10")
        stats_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.points_label = ttk.Label(stats_frame, text="💰 Points: 0", font=("Arial", 16, "bold"))
        self.points_label.grid(row=0, column=0, sticky=tk.W)
        
        self.production_label = ttk.Label(stats_frame, text="📈 Production/sec: 0", font=("Arial", 14))
        self.production_label.grid(row=1, column=0, sticky=tk.W)
        
        self.clicks_label = ttk.Label(stats_frame, text="🖱️  Clics: 0", font=("Arial", 12))
        self.clicks_label.grid(row=2, column=0, sticky=tk.W)
        
        self.prestige_label = ttk.Label(stats_frame, text="⭐ Prestige: Level 0", font=("Arial", 12))
        self.prestige_label.grid(row=3, column=0, sticky=tk.W)
        
        # === CLICK BUTTON ===
        click_frame = ttk.Frame(main_frame)
        click_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.click_button = tk.Button(click_frame, text="🖱️ CLIQUER", font=("Arial", 18, "bold"),
                                       command=self.click, bg="#FFD700", fg="black", width=20, height=2)
        self.click_button.pack()
        
        # === GENERATORS ===
        gen_frame = ttk.LabelFrame(main_frame, text="🏭 GÉNÉRATEURS", padding="10")
        gen_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.gen_buttons = {}
        for i, (gen_id, gen_data) in enumerate(self.generators.items()):
            frame = ttk.Frame(gen_frame)
            frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
            
            label = ttk.Label(frame, text=f"{gen_data['icon']} {gen_data['name']}", width=15)
            label.grid(row=0, column=0, sticky=tk.W)
            
            self.gen_buttons[gen_id] = {
                "button": tk.Button(frame, text=f"Acheter ({gen_data['cost']})", 
                                   command=lambda g=gen_id: self.buy_generator(g)),
                "count_label": ttk.Label(frame, text="Possédés: 0", width=15)
            }
            
            self.gen_buttons[gen_id]["button"].grid(row=0, column=1, padx=5)
            self.gen_buttons[gen_id]["count_label"].grid(row=0, column=2, sticky=tk.E)
        
        # === UPGRADES ===
        upg_frame = ttk.LabelFrame(main_frame, text="⚡ UPGRADES", padding="10")
        upg_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.upgrade_buttons = {}
        for i, (upgrade_id, upgrade_data) in enumerate(UPGRADES.items()):
            frame = ttk.Frame(upg_frame)
            frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
            
            label = ttk.Label(frame, text=upgrade_data['name'], width=15)
            label.grid(row=0, column=0, sticky=tk.W)
            
            self.upgrade_buttons[upgrade_id] = {
                "button": tk.Button(frame, text="Acheter", 
                                   command=lambda u=upgrade_id: self.buy_upgrade(u)),
                "level_label": ttk.Label(frame, text="Lvl: 0", width=8)
            }
            
            self.upgrade_buttons[upgrade_id]["button"].grid(row=0, column=1, padx=5)
            self.upgrade_buttons[upgrade_id]["level_label"].grid(row=0, column=2, sticky=tk.E)
        
        # === MENU ===
        menu_frame = ttk.Frame(main_frame)
        menu_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(menu_frame, text="🏆 Achievements", command=self.show_achievements).pack(side=tk.LEFT, padx=5)
        ttk.Button(menu_frame, text="⭐ Prestige", command=self.show_prestige).pack(side=tk.LEFT, padx=5)
        ttk.Button(menu_frame, text="💾 Sauvegarder", command=self.save_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(menu_frame, text="❌ Quitter", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Configure column weights for resizing
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
    
    def click(self):
        """Le joueur clique"""
        click_value = 1.0 * self.prestige_system.get_click_bonus()
        self.points += click_value
        self.total_clicks += 1
        self.update_ui()
    
    def buy_generator(self, generator_id):
        """Achète un générateur"""
        gen = self.generators[generator_id]
        cost = gen["cost"]
        
        if self.points >= cost:
            self.points -= cost
            gen["owned"] += 1
            messagebox.showinfo("Succès", f"✅ {gen['name']} acheté!")
            self.update_ui()
        else:
            messagebox.showerror("Erreur", f"❌ Pas assez de points!\nBesoin: {cost}, Tu as: {int(self.points)}")
    
    def buy_upgrade(self, upgrade_id):
        """Achète un upgrade"""
        success, message = self.upgrade_system.buy_upgrade(upgrade_id, self.points)
        
        if success:
            self.points -= message
            messagebox.showinfo("Succès", "✅ Upgrade acheté!")
            self.update_ui()
        else:
            messagebox.showerror("Erreur", f"❌ {message}")
    
    def calculate_production_per_second(self):
        """Calcule la production par seconde"""
        total = 0
        for gen_id, gen in self.generators.items():
            multiplier = self.upgrade_system.get_production_multiplier(gen_id)
            production = gen["owned"] * gen["production"] * multiplier
            total += production
        
        prestige_bonus = 1.0 + self.prestige_system.get_production_bonus()
        total *= prestige_bonus
        
        return total
    
    def update_production(self):
        """Met à jour la production automatique"""
        now = datetime.now()
        elapsed = (now - self.last_update_time).total_seconds()
        
        production_per_sec = self.calculate_production_per_second()
        self.points += production_per_sec * elapsed
        
        self.last_update_time = now
    
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
            for achievement_id in newly_unlocked:
                achievement = ACHIEVEMENTS[achievement_id]
                reward = achievement.get("points", 0)
                self.points += reward
                messagebox.showinfo("🎉 ACHIEVEMENT", 
                                  f"{achievement['icon']} {achievement['name']}\n+{reward} points")
    
    def update_ui(self):
        """Met à jour l'interface"""
        production = self.calculate_production_per_second()
        
        self.points_label.config(text=f"💰 Points: {int(self.points):,}")
        self.production_label.config(text=f"📈 Production/sec: {production:.0f}")
        self.clicks_label.config(text=f"🖱️  Clics: {self.total_clicks}")
        
        if self.prestige_system.prestige_level > 0:
            bonus = self.prestige_system.get_production_bonus() * 100
            self.prestige_label.config(text=f"⭐ Prestige: Level {self.prestige_system.prestige_level} (+{bonus:.0f}%)")
        
        # Mettre à jour les générateurs
        for gen_id, gen_data in self.generators.items():
            self.gen_buttons[gen_id]["count_label"].config(text=f"Possédés: {gen_data['owned']}")
        
        # Mettre à jour les upgrades
        for upgrade_id, upgrade_data in UPGRADES.items():
            level = self.upgrade_system.upgrades[upgrade_id]["level"]
            max_level = upgrade_data.get("max_level", 1)
            self.upgrade_buttons[upgrade_id]["level_label"].config(text=f"Lvl: {level}/{max_level}")
    
    def show_achievements(self):
        """Affiche les achievements"""
        window = tk.Toplevel(self.root)
        window.title("🏆 Achievements")
        window.geometry("500x400")
        
        frame = ttk.Frame(window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        unlocked_count = self.achievement_system.get_unlocked_count()
        total_count = len(ACHIEVEMENTS)
        
        title = ttk.Label(scrollable_frame, text=f"🏆 Achievements: {unlocked_count}/{total_count}", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        for achievement_id, achievement_data in ACHIEVEMENTS.items():
            is_unlocked = self.achievement_system.is_unlocked(achievement_id)
            icon = "✅" if is_unlocked else "🔒"
            
            text = f"{icon} {achievement_data['icon']} {achievement_data['name']}\n{achievement_data['description']}"
            if is_unlocked:
                text += f"\n💎 +{achievement_data['points']} points"
            
            label = ttk.Label(scrollable_frame, text=text, wraplength=400, justify=tk.LEFT)
            label.pack(padx=10, pady=5, anchor=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_prestige(self):
        """Affiche le menu prestige"""
        window = tk.Toplevel(self.root)
        window.title("⭐ Prestige")
        window.geometry("400x300")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="⭐ PRESTIGE SYSTEM", font=("Arial", 16, "bold")).pack(pady=10)
        
        prestige_points = self.prestige_system.calculate_prestige_points(self.points)
        can_prestige = self.prestige_system.can_prestige(self.points)
        
        info_text = f"""
Prestige Level: {self.prestige_system.prestige_level}
Production Bonus: +{self.prestige_system.get_production_bonus()*100:.0f}%
Total Prestige Points: {self.prestige_system.total_prestige_points}

Points nécessaires: {PRESTIGE_RESET_COST:,}
Points que tu gagneras: {prestige_points}
        """
        
        ttk.Label(frame, text=info_text, justify=tk.LEFT, font=("Arial", 11)).pack(pady=10)
        
        if can_prestige:
            ttk.Label(frame, text="⚠️  Le prestige réinitialisera tous tes générateurs!", 
                     font=("Arial", 10), foreground="red").pack(pady=5)
            ttk.Button(frame, text="Confirmer Prestige", 
                      command=lambda: self.do_prestige(window)).pack(pady=10)
        else:
            manque = PRESTIGE_RESET_COST - int(self.points)
            ttk.Label(frame, text=f"❌ Pas assez de points (manque: {manque:,})", 
                     foreground="red").pack(pady=10)
    
    def do_prestige(self, window):
        """Effectue un prestige"""
        success, prestige_points = self.prestige_system.prestige(self.points)
        
        if success:
            self.points = 0
            for gen in self.generators.values():
                gen["owned"] = 0
            self.upgrade_system = UpgradeSystem()
            
            messagebox.showinfo("✨ Prestige", 
                              f"Prestige effectué!\n+{prestige_points} prestige points")
            self.update_ui()
            window.destroy()
        else:
            messagebox.showerror("Erreur", f"❌ {prestige_points}")
    
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
        
        messagebox.showinfo("Succès", "💾 Jeu sauvegardé!")
    
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
            except Exception as e:
                print(f"Erreur lors du chargement: {e}")
    
    def update_game(self):
        """Boucle de mise à jour du jeu"""
        self.update_production()
        self.check_achievements()
        self.update_ui()
        
        self.root.after(100, self.update_game)


def main():
    """Lance le jeu"""
    root = tk.Tk()
    app = IdleGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
