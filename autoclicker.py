import sys
import time
import threading
import pyautogui
import keyboard
import customtkinter as ctk

# 안전장치 설정
pyautogui.FAILSAFE = True
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AutoClickerApp:
    def __init__(self):
        self.running = False
        self.start_time = 0
        self.click_count = 0
        self.total_duration = 0
        self.interval_sec = 0
        self.show_stats = False
        
        # 보조키(Modifier) 옵션
        self.modifiers = {
            "None": "", "Ctrl": "ctrl+", "Shift": "shift+", "Alt": "alt+",
            "Ctrl+Shift": "ctrl+shift+", "Ctrl+Alt": "ctrl+alt+",
            "Shift+Alt": "shift+alt+", "Ctrl+Shift+Alt": "ctrl+shift+alt+"
        }
        
        # 기본키(Key) 옵션
        self.keys = [
            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "SPACE", "ENTER", "HOME", "END", "INSERT", "DELETE", "PAGE UP", "PAGE DOWN"
        ]
        
        self.current_hotkey_str = ""
        self.run_gui()

    def update_hotkey_binding(self):
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        mod = self.modifiers[self.modifier_var.get()]
        key = self.key_var.get().lower().replace(" ", "")
        self.current_hotkey_str = f"{mod}{key}"
        try:
            keyboard.add_hotkey(self.current_hotkey_str, self.toggle_running, suppress=True)
        except:
            pass

    def parse_time(self, entries):
        try:
            h = float(entries['H'].get() or 0)
            m = float(entries['M'].get() or 0)
            s = float(entries['S'].get() or 0)
            ms = float(entries['ms'].get() or 0)
            return h*3600 + m*60 + s + ms/1000
        except ValueError:
            return 0

    def format_time(self, seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def click_logic(self, interval_sec, duration_sec):
        self.start_time = time.time()
        self.click_count = 0
        try:
            while self.running:
                elapsed = time.time() - self.start_time
                if duration_sec > 0 and elapsed >= duration_sec:
                    self.running = False
                    self.root.after(0, self.root.destroy)
                    return

                # Jiggle & Click
                pos = pyautogui.position()
                pyautogui.moveRel(1, 0, duration=0.05)
                pyautogui.moveTo(pos.x, pos.y, duration=0.05)
                pyautogui.click()
                self.click_count += 1
                
                # UI 업데이트 (통계 전용)
                self.root.after(0, self.refresh_stats_ui, elapsed, duration_sec)

                wait_until = time.time() + interval_sec
                while time.time() < wait_until and self.running:
                    time.sleep(0.05)
                    if duration_sec > 0 and (time.time() - self.start_time) >= duration_sec:
                        self.running = False
                        self.root.after(0, self.root.destroy)
                        return
        except:
            self.running = False
        finally:
            self.update_ui_state()

    def refresh_stats_ui(self, elapsed, duration_sec):
        if not self.running: return
        self.total_clicks_val.configure(text=f"{self.click_count} 회")
        self.elapsed_val.configure(text=self.format_time(elapsed))
        
        if duration_sec > 0:
            remaining = max(0, duration_sec - elapsed)
            self.rem_time_val.configure(text=self.format_time(remaining))
            # 남은 클릭 수 추정
            rem_clicks = int(remaining / self.interval_sec) if self.interval_sec > 0 else 0
            self.rem_clicks_val.configure(text=f"약 {rem_clicks} 회")
        else:
            self.rem_time_val.configure(text="무제한")
            self.rem_clicks_val.configure(text="무제한")

    def toggle_running(self):
        if not self.running:
            self.interval_sec = self.parse_time(self.interval_entries)
            self.total_duration = self.parse_time(self.duration_entries)
            if self.interval_sec <= 0: return
            self.running = True
            threading.Thread(target=self.click_logic, args=(self.interval_sec, self.total_duration), daemon=True).start()
        else:
            self.running = False
        self.root.after(0, self.update_ui_state)

    def update_ui_state(self):
        if not hasattr(self, 'start_btn'): return
        display_name = self.current_hotkey_str.upper().replace("+", " + ")
        if self.running:
            self.start_btn.configure(text=f"중지 ({display_name})", fg_color="#E74C3C")
            self.status_label.configure(text="● ACTIVE", text_color="#2ECC71")
        else:
            self.start_btn.configure(text=f"시작 ({display_name})", fg_color="#3498DB")
            self.status_label.configure(text="○ READY", text_color="#95A5A6")

    def toggle_stats_view(self):
        self.show_stats = not self.show_stats
        if self.show_stats:
            self.stats_frame.pack(pady=10, padx=20, fill="x", after=self.toggle_btn)
            self.toggle_btn.configure(text="통계 숨기기 ▲")
            self.root.geometry("480x820")
        else:
            self.stats_frame.pack_forget()
            self.toggle_btn.configure(text="통계 보기 ▼")
            self.root.geometry("480x620")

    def create_time_input(self, parent, label_text, default_s=0):
        frame = ctk.CTkFrame(parent)
        frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(frame, text=label_text, font=("Pretendard", 14, "bold")).pack(pady=5)
        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(pady=5)
        entries = {}
        for i, (code, name) in enumerate([("H", "시"), ("M", "분"), ("S", "초"), ("ms", "ms")]):
            f = ctk.CTkFrame(grid, fg_color="transparent")
            f.grid(row=0, column=i, padx=5)
            e = ctk.CTkEntry(f, width=65, justify="center")
            e.pack()
            e.insert(0, str(default_s) if code == "S" else "0")
            entries[code] = e
            ctk.CTkLabel(f, text=name, font=("Pretendard", 10)).pack()
        return entries

    def run_gui(self):
        self.root = ctk.CTk()
        self.root.title("AutoClicker Pro Master")
        self.root.geometry("480x620")
        self.root.resizable(False, False)

        ctk.CTkLabel(self.root, text="Discord AutoClicker", font=("Pretendard", 28, "bold")).pack(pady=20)

        self.interval_entries = self.create_time_input(self.root, "1. 클릭 간격 (Interval)", 5)
        self.duration_entries = self.create_time_input(self.root, "2. 총 실행 시간 (Timer)", 0)

        group_3 = ctk.CTkFrame(self.root)
        group_3.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(group_3, text="3. 단축키 설정", font=("Pretendard", 14, "bold")).pack(pady=5)
        combo_f = ctk.CTkFrame(group_3, fg_color="transparent")
        combo_f.pack(pady=5, padx=10, fill="x")
        self.modifier_var = ctk.StringVar(value="None")
        ctk.CTkOptionMenu(combo_f, values=list(self.modifiers.keys()), variable=self.modifier_var, command=lambda _: self.on_selection_change(), width=140).pack(side="left", padx=5, expand=True)
        self.key_var = ctk.StringVar(value="F9")
        ctk.CTkOptionMenu(combo_f, values=self.keys, variable=self.key_var, command=lambda _: self.on_selection_change(), width=140).pack(side="left", padx=5, expand=True)

        self.status_label = ctk.CTkLabel(self.root, text="○ READY", font=("Pretendard", 18, "bold"), text_color="#95A5A6")
        self.status_label.pack(pady=10)
        self.start_btn = ctk.CTkButton(self.root, text="시작 (F9)", height=60, font=("Pretendard", 20, "bold"), command=self.toggle_running)
        self.start_btn.pack(pady=10, padx=60, fill="x")

        # 통계 토글 버튼
        self.toggle_btn = ctk.CTkButton(self.root, text="통계 보기 ▼", fg_color="transparent", text_color="gray", hover_color="#2b2b2b", command=self.toggle_stats_view)
        self.toggle_btn.pack(pady=5)

        # 통계 프레임 (초기 숨김)
        self.stats_frame = ctk.CTkFrame(self.root, fg_color="#2b2b2b")
        stats_grid = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        stats_grid.pack(pady=10, padx=10, fill="x")
        
        self.total_clicks_val = self.create_stat_row(stats_grid, "총 클릭 횟수:", "0 회", 0)
        self.elapsed_val = self.create_stat_row(stats_grid, "경과 시간:", "00:00:00", 1)
        self.rem_time_val = self.create_stat_row(stats_grid, "남은 시간:", "무제한", 2)
        self.rem_clicks_val = self.create_stat_row(stats_grid, "남은 클릭(예상):", "무제한", 3)

        self.update_hotkey_binding()
        self.root.mainloop()

    def create_stat_row(self, parent, label, initial_val, row):
        ctk.CTkLabel(parent, text=label, font=("Pretendard", 12)).grid(row=row, column=0, sticky="w", padx=10, pady=2)
        val_label = ctk.CTkLabel(parent, text=initial_val, font=("Pretendard", 12, "bold"), text_color="#3498DB")
        val_label.grid(row=row, column=1, sticky="e", padx=10, pady=2)
        parent.grid_columnconfigure(1, weight=1)
        return val_label

    def on_selection_change(self):
        self.update_hotkey_binding()
        self.update_ui_state()

if __name__ == "__main__":
    AutoClickerApp()
