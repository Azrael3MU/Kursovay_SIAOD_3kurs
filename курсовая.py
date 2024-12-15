import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import random
from datetime import datetime, timedelta

class RouteScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Планировщик маршрутов")
        self.root.geometry("1280x720")
        self.root.resizable(True, True)
        self.type_a_drivers = []
        self.type_b_drivers = []
        self.route_options = ['до конечной и обратно', 'до конечной']
        self.shift_duration_a = 8
        self.shift_duration_b = 12
        self.travel_duration_minutes = 60
        self.workday_start = '06:00'
        self.workday_end = '03:00'
        
        # Установка темы
        self.theme_style = tb.Style(theme="cyborg")  # Выберите подходящую тему
        
        # Основной контейнер для контента с рамкой
        # Добавляем отступ сверху для центрирования по вертикали
        self.main_content_frame = tb.Frame(self.root, padding=20, relief='groove', borderwidth=2)
        self.main_content_frame.pack(padx=50, pady=(100, 50))  # Увеличен верхний отступ
        
        # Основные фреймы для разных разделов внутри main_content_frame
        self.setup_frames()
        
        # Навигационная панель под основным контентом
        self.setup_navigation_bar()
        
        # Статусная строка внизу окна
        self.setup_status_bar()
    
    def setup_navigation_bar(self):
        nav_frame = tb.Frame(self.root, bootstyle=DARK)
        nav_frame.pack(pady=(0, 20))  # Добавляем отступ сверху
        
        # Кнопки навигации с желтым цветом
        register_btn = tb.Button(
            nav_frame,
            text="Запись",
            command=self.show_registration,
            bootstyle='warning',  # Желтый цвет
            width=20
        )
        register_btn.pack(side=LEFT, padx=5, pady=5)
        
        configure_btn = tb.Button(
            nav_frame,
            text="Конфигурация маршрутов",
            command=self.show_configuration,
            bootstyle='warning',  # Желтый цвет
            width=20
        )
        configure_btn.pack(side=LEFT, padx=5, pady=5)
        
        schedule_btn = tb.Button(
            nav_frame,
            text="Формирование графика",
            command=self.show_schedule_creation,
            bootstyle='warning',  # Желтый цвет
            width=20
        )
        schedule_btn.pack(side=LEFT, padx=5, pady=5)
    
    def setup_frames(self):
        # Фрейм записи водителей
        self.registration_frame = tb.Frame(self.main_content_frame)
        
        registration_title = tb.Label(
            self.registration_frame,
            text="Запись водителя",
            font=("Arial", 24, "bold"),
            bootstyle=PRIMARY
        )
        registration_title.pack(pady=20)
        
        registration_input = tb.Frame(self.registration_frame)
        registration_input.pack(pady=10, padx=20)
        
        # ФИО водителя
        tb.Label(registration_input, text="ФИО водителя:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.driver_name_entry = tb.Entry(registration_input, width=40, font=("Arial", 14))
        self.driver_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Тип водителя
        tb.Label(registration_input, text="Тип водителя:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.driver_type_var = tb.StringVar(value="A")
        self.driver_type_menu = tb.Combobox(
            registration_input,
            textvariable=self.driver_type_var,
            values=["A", "B"],
            state="readonly",
            width=38,
            font=("Arial", 14),
            bootstyle='warning'  # Применяем стиль к Combobox
        )
        self.driver_type_menu.grid(row=1, column=1, padx=10, pady=10)
        
        # Кнопка записи
        register_driver_button = tb.Button(
            self.registration_frame,
            text="Добавить",
            command=self.register_driver,
            bootstyle='warning',  # Желтый цвет
            width=20
        )
        register_driver_button.pack(pady=20)
        
        # Фрейм конфигурации маршрутов
        self.configuration_frame = tb.Frame(self.main_content_frame)
        
        config_title = tb.Label(
            self.configuration_frame,
            text="Конфигурация маршрутов",
            font=("Arial", 24, "bold"),
            bootstyle=PRIMARY
        )
        config_title.pack(pady=20)
        
        config_input = tb.Frame(self.configuration_frame)
        config_input.pack(pady=10, padx=20)
        
        # Количество маршрутов в день
        tb.Label(config_input, text="Количество маршрутов в день:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.total_routes_entry = tb.Entry(config_input, width=40, font=("Arial", 14))
        self.total_routes_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Длительность маршрута
        tb.Label(config_input, text="Длительность маршрута (мин):", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.route_length_entry = tb.Entry(config_input, width=40, font=("Arial", 14))
        self.route_length_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Кнопки конфигурации
        buttons_frame = tb.Frame(self.configuration_frame)
        buttons_frame.pack(pady=20)
        
        apply_route_config_button = tb.Button(
            buttons_frame,
            text="Сохранить настройки",
            command=self.set_route_parameters,
            bootstyle='warning',  # Желтый цвет
            width=20
        )
        apply_route_config_button.grid(row=0, column=0, padx=10)
        
        clear_data_button = tb.Button(
            buttons_frame,
            text="Удалить записи",
            command=self.clear_all_records,
            bootstyle='warning',  # Желтый цвет
            width=20
        )
        clear_data_button.grid(row=0, column=1, padx=10)
        
        # Фрейм формирования графика
        self.schedule_frame = tb.Frame(self.main_content_frame)
        
        schedule_title = tb.Label(
            self.schedule_frame,
            text="Формирование графика",
            font=("Arial", 24, "bold"),
            bootstyle=PRIMARY
        )
        schedule_title.pack(pady=20)
        
        schedule_input = tb.Frame(self.schedule_frame)
        schedule_input.pack(pady=10, padx=20)
        
        # Выбор дня
        tb.Label(schedule_input, text="Выберите день:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.selected_day_var = tb.StringVar(value="Понедельник")
        self.selected_day_menu = tb.Combobox(
            schedule_input,
            textvariable=self.selected_day_var,
            values=["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
            state="readonly",
            width=38,
            font=("Arial", 14),
            bootstyle='warning'  # Применяем стиль к Combobox
        )
        self.selected_day_menu.grid(row=0, column=1, padx=10, pady=10)
        
        # Кнопки генерации графика
        schedule_buttons_frame = tb.Frame(self.schedule_frame)
        schedule_buttons_frame.pack(pady=20)
        
        generate_timetable_button = tb.Button(
            schedule_buttons_frame,
            text="Стандартное расписание",
            command=self.start_schedule_creation,
            bootstyle='warning',  # Желтый цвет
            width=25
        )
        generate_timetable_button.grid(row=0, column=0, padx=10)
        
        generate_genetic_timetable_button = tb.Button(
            schedule_buttons_frame,
            text="Алгоритмическое расписание",
            command=self.start_genetic_schedule,
            bootstyle='warning',  # Желтый цвет
            width=25
        )
        generate_genetic_timetable_button.grid(row=0, column=1, padx=10)
        
        # Показываем начальный раздел
        self.show_registration()
    
    def setup_status_bar(self):
        self.status_frame = tb.Frame(self.root)
        self.status_frame.pack(side=BOTTOM, fill=X)
        self.status_label = tb.Label(
            self.status_frame,
            text="Добро пожаловать в Планировщик маршрутов!",
            font=("Arial", 12),
            bootstyle=INFO
        )
        self.status_label.pack(pady=5)
    
    def show_registration(self):
        self.hide_all_frames()
        self.registration_frame.pack(fill=BOTH, expand=True)
    
    def show_configuration(self):
        self.hide_all_frames()
        self.configuration_frame.pack(fill=BOTH, expand=True)
    
    def show_schedule_creation(self):
        self.hide_all_frames()
        self.schedule_frame.pack(fill=BOTH, expand=True)
    
    def hide_all_frames(self):
        self.registration_frame.pack_forget()
        self.configuration_frame.pack_forget()
        self.schedule_frame.pack_forget()
    
    def register_driver(self):
        name = self.driver_name_entry.get().strip()
        driver_type = self.driver_type_var.get()
        if not name:
            messagebox.showerror("Ошибка", "Введите имя водителя.")
            return
        if driver_type == "A":
            if name in self.type_a_drivers:
                messagebox.showwarning("Предупреждение", f"Водитель '{name}' уже зарегистрирован как Тип A.")
                return
            self.type_a_drivers.append(name)
        else:
            if name in self.type_b_drivers:
                messagebox.showwarning("Предупреждение", f"Водитель '{name}' уже зарегистрирован как Тип B.")
                return
            self.type_b_drivers.append(name)
        self.driver_name_entry.delete(0, tb.END)
        self.refresh_status(f"Водитель '{name}' добавлен.", SUCCESS)
    
    def clear_all_records(self):
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все записи?")
        if confirm:
            self.total_routes_entry.delete(0, tb.END)
            self.route_length_entry.delete(0, tb.END)
            self.driver_name_entry.delete(0, tb.END)
            self.type_a_drivers.clear()
            self.type_b_drivers.clear()
            self.refresh_status("Записи удалены.", WARNING)
    
    def set_route_parameters(self):
        try:
            self.travel_duration_minutes = int(self.route_length_entry.get())
            self.refresh_status(f"Длительность маршрута установлена на {self.travel_duration_minutes} минут.", SUCCESS)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число для длительности маршрута.")
    
    def refresh_status(self, message, color=INFO):
        self.status_label.config(text=message, bootstyle=color)
        self.status_label.after(5000, lambda: self.status_label.config(text=""))
    
    def is_weekend(self, selected_day):
        return selected_day in ['Суббота', 'Воскресенье']
    
    def calculate_route_completion(self, start_time, route_time):
        start_time_obj = datetime.strptime(start_time, "%H:%M")
        end_time_obj = start_time_obj + timedelta(minutes=route_time)
        return end_time_obj.strftime("%H:%M")
    
    def standardize_time_interval(self, start_str, end_str):
        start = datetime.strptime(start_str, "%H:%M")
        end = datetime.strptime(end_str, "%H:%M")
        if end < start:
            end += timedelta(days=1)
        return start, end
    
    def detect_time_overlap(self, start_time, end_time, busy_times):
        s, e = self.standardize_time_interval(start_time, end_time)
        for (bs, be) in busy_times:
            b_s, b_e = self.standardize_time_interval(bs, be)
            if s < b_e and e > b_s:
                return True
        return False
    
    def find_free_periods(self, driver_busy_times, route_time, break_time):
        free_slots = []
        for driver, periods in driver_busy_times.items():
            normalized_periods = []
            for (st, ft) in periods:
                s_t, f_t = self.standardize_time_interval(st, ft)
                normalized_periods.append((s_t, f_t))
            normalized_periods.sort(key=lambda x: x[0])
            current = datetime.strptime("06:00", "%H:%M")
            work_end = datetime.strptime("03:00", "%H:%M") + timedelta(days=1)
            for (st, et) in normalized_periods:
                if (st - current).total_seconds() / 60 >= route_time + break_time:
                    free_slots.append((current.strftime("%H:%M"), st.strftime("%H:%M")))
                current = et
            if (work_end - current).total_seconds() / 60 >= route_time + break_time:
                free_slots.append((current.strftime("%H:%M"), work_end.strftime("%H:%M")))
        return free_slots
    
    def calculate_additional_driver_needs(self, num_routes, driver_list, shift_duration):
        max_routes_per_driver = int(shift_duration * 60 / self.travel_duration_minutes)
        required_drivers = (num_routes + max_routes_per_driver - 1) // max_routes_per_driver
        if len(driver_list) >= required_drivers:
            return 0
        else:
            return required_drivers - len(driver_list)
    
    def can_assign_route(self, candidate_start_time, route_time, driver, driver_busy_times, driver_worked_hours, driver_route_counts, min_break_time):
        candidate_end_time = self.calculate_route_completion(candidate_start_time, route_time)
        if self.detect_time_overlap(candidate_start_time, candidate_end_time, driver_busy_times[driver]):
            return False
        if driver_busy_times[driver]:
            last_start, last_end = driver_busy_times[driver][-1]
            last_end_obj = datetime.strptime(last_end, "%H:%M")
            last_start_obj = datetime.strptime(last_start, "%H:%M")
            if last_end_obj < last_start_obj:
                last_end_obj += timedelta(days=1)
            candidate_start_obj = datetime.strptime(candidate_start_time, "%H:%M")
            if candidate_start_obj < last_end_obj:
                return False
            if (candidate_start_obj - last_end_obj).total_seconds() / 60 < min_break_time:
                return False
        worked_hours = driver_worked_hours[driver]
        if driver in self.type_a_drivers and worked_hours >= self.shift_duration_a:
            return False
        if driver in self.type_b_drivers and worked_hours >= self.shift_duration_b:
            return False
        candidate_end_obj = datetime.strptime(candidate_end_time, "%H:%M")
        if candidate_end_obj < datetime.strptime(candidate_start_time, "%H:%M"):
            candidate_end_obj += timedelta(days=1)
        end_work_obj = datetime.strptime("03:00", "%H:%M") + timedelta(days=1)
        if candidate_end_obj > end_work_obj:
            return False
        return True
    
    def allocate_driver_to_route(self, route_time, break_time, min_break_time, driver_list, driver_busy_times, driver_worked_hours, selected_day, driver_route_counts):
        for _ in range(50):
            free_slots = self.find_free_periods(driver_busy_times, route_time, break_time)
            if not free_slots:
                return None
            slot_start, slot_end = random.choice(free_slots)
            slot_start_obj = datetime.strptime(slot_start, "%H:%M")
            slot_end_obj = datetime.strptime(slot_end, "%H:%M")
            if slot_end_obj < slot_start_obj:
                slot_end_obj += timedelta(days=1)
            max_start = (slot_end_obj - slot_start_obj).total_seconds() / 60 - route_time
            if max_start < 0:
                continue
            offset = random.randint(0, int(max_start))
            candidate_start_obj = slot_start_obj + timedelta(minutes=offset)
            candidate_start = candidate_start_obj.strftime("%H:%M")
            random.shuffle(driver_list)
            for driver in driver_list:
                if driver in self.type_a_drivers and self.is_weekend(selected_day):
                    continue
                if self.can_assign_route(candidate_start, route_time, driver, driver_busy_times, driver_worked_hours, driver_route_counts, min_break_time):
                    return (driver, candidate_start)
        return None
    
    def generate_genetic_schedule_attempt(self, driver_list, shift_duration, num_routes, selected_day, break_time=10, min_break_time=30):
        available_drivers = list(driver_list)
        random.shuffle(available_drivers)
        driver_busy_times = {driver: [] for driver in available_drivers}
        driver_worked_hours = {driver: 0 for driver in available_drivers}
        driver_route_counts = {driver: 0 for driver in available_drivers}
        schedule = []
        start_time = datetime.strptime("06:00", "%H:%M")
        end_work_time = datetime.strptime("03:00", "%H:%M") + timedelta(days=1)
        for _ in range(num_routes):
            placed = False
            candidate_start_time = start_time
            candidate_end_time = candidate_start_time + timedelta(minutes=self.travel_duration_minutes)
            if candidate_end_time > end_work_time:
                route_type_selected = random.choice(self.route_options)
                route_type = f"{route_type_selected} (доп рейс)"
            else:
                route_type = random.choice(self.route_options)
            for driver in available_drivers:
                if self.can_assign_route(candidate_start_time.strftime("%H:%M"), self.travel_duration_minutes, driver, driver_busy_times, driver_worked_hours, driver_route_counts, min_break_time):
                    schedule.append({
                        'Водитель': driver,
                        'Тип маршрута': route_type,
                        'Время начала': candidate_start_time.strftime("%H:%M"),
                        'Время окончания': candidate_end_time.strftime("%H:%M"),
                        'Маршрутов за смену': driver_route_counts[driver] + 1
                    })
                    driver_busy_times[driver].append((candidate_start_time.strftime("%H:%M"), candidate_end_time.strftime("%H:%M")))
                    driver_route_counts[driver] += 1
                    driver_worked_hours[driver] += self.travel_duration_minutes / 60
                    placed = True
                    break
            if not placed:
                break
            start_time = candidate_end_time + timedelta(minutes=break_time)
            if start_time >= end_work_time:
                start_time = datetime.strptime("06:00", "%H:%M")
                route_type = f"{random.choice(self.route_options)} (доп рейс)"
        return schedule, len(schedule)
    
    def assess_schedule_quality(self, schedule):
        return len(schedule)
    
    def execute_crossover(self, parent1, parent2):
        if not parent1 or not parent2:
            return parent1, parent2
        crossover_point = len(parent1) // 2
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    
    def execute_mutation(self, schedule, driver_list, break_time=10):
        if not schedule:
            return schedule
        mutated_schedule = schedule.copy()
        mutation_point = random.randint(0, len(mutated_schedule) - 1)
        new_driver = random.choice(driver_list)
        mutated_schedule[mutation_point]['Водитель'] = new_driver
        if random.random() < 0.5:
            original_start = mutated_schedule[mutation_point]['Время начала']
            original_end = mutated_schedule[mutation_point]['Время окончания']
            try:
                start_obj = datetime.strptime(original_start, "%H:%M") + timedelta(minutes=random.randint(-15, 15))
                end_obj = datetime.strptime(original_end, "%H:%M") + timedelta(minutes=random.randint(-15, 15))
                mutated_schedule[mutation_point]['Время начала'] = start_obj.strftime("%H:%M")
                mutated_schedule[mutation_point]['Время окончания'] = end_obj.strftime("%H:%M")
            except ValueError:
                pass
        return mutated_schedule
    
    def display_generated_timetable(self, result_window, schedule_df, title_text="Итоговое расписание"):
        result_window.title(title_text)
        result_window.geometry("800x600")
        result_window.resizable(True, True)
        if not schedule_df.empty:
            frame = tb.Frame(result_window)
            frame.pack(fill='both', expand=True, padx=20, pady=20)
            scrollbar = ttk.Scrollbar(frame, orient="vertical")
            scrollbar.pack(side='right', fill='y')
            columns = list(schedule_df.columns)
            tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')
            for index, row in schedule_df.iterrows():
                tree.insert("", "end", values=list(row))
            scrollbar.config(command=tree.yview)
            tree.pack(fill='both', expand=True)
        else:
            message = "Не удалось сформировать расписание.\nДобавьте водителей или уменьшите количество рейсов."
            messagebox.showerror("Ошибка", message)
    
    def build_optimized_timetable(self, driver_list, shift_duration, num_routes, selected_day, parent_window, break_time=10, min_break_time=30):
        additional_needed = self.calculate_additional_driver_needs(num_routes, driver_list, shift_duration)
        if additional_needed > 0:
            message = f"Недостаточно сотрудников.\nНужно добавить ещё {additional_needed} водителей или уменьшить количество рейсов."
            messagebox.showerror("Ошибка", message)
            return
        schedule = []
        driver_busy_times = {d: [] for d in driver_list}
        driver_worked_hours = {d: 0 for d in driver_list}
        driver_route_counts = {d: 0 for d in driver_list}
        current_time = datetime.strptime("06:00", "%H:%M")
        work_end = datetime.strptime("03:00", "%H:%M") + timedelta(days=1)
        for _ in range(num_routes):
            route_type = random.choice(self.route_options)
            actual_time = self.travel_duration_minutes * 2 if 'обратно' in route_type else self.travel_duration_minutes
            candidate_start_str = current_time.strftime("%H:%M")
            candidate_end_str = self.calculate_route_completion(candidate_start_str, actual_time)
            candidate_end_obj = datetime.strptime(candidate_end_str, "%H:%M")
            if candidate_end_obj < current_time:
                candidate_end_obj += timedelta(days=1)
            if candidate_end_obj > work_end:
                final_type = f"{route_type} (доп рейс)"
                result = self.allocate_driver_to_route(actual_time, break_time, min_break_time, driver_list, driver_busy_times, driver_worked_hours, selected_day, driver_route_counts)
                if result is None:
                    message = "Расписание не утверждено.\nДобавьте сотрудников или уменьшите количество рейсов."
                    messagebox.showerror("Ошибка", message)
                    return
                else:
                    driver, slot_start = result
                    cend = self.calculate_route_completion(slot_start, actual_time)
                    worked_minutes = (datetime.strptime(cend, "%H:%M") - datetime.strptime(slot_start, "%H:%M")).seconds / 60
                    schedule.append({
                        'Водитель': driver,
                        'Тип маршрута': final_type,
                        'Время начала': slot_start,
                        'Время окончания': cend,
                        'Маршрутов за смену': driver_route_counts[driver] + 1
                    })
                    driver_busy_times[driver].append((slot_start, cend))
                    driver_worked_hours[driver] += worked_minutes / 60
            else:
                placed = False
                copy_drivers = list(driver_list)
                random.shuffle(copy_drivers)
                for driver in copy_drivers:
                    if driver in self.type_a_drivers and self.is_weekend(selected_day):
                        continue
                    if self.can_assign_route(candidate_start_str, actual_time, driver, driver_busy_times, driver_worked_hours, driver_route_counts, min_break_time):
                        worked_minutes = (candidate_end_obj - datetime.strptime(candidate_start_str, "%H:%M")).seconds / 60
                        schedule.append({
                            'Водитель': driver,
                            'Тип маршрута': route_type,
                            'Время начала': candidate_start_str,
                            'Время окончания': candidate_end_str,
                            'Маршрутов за смену': driver_route_counts[driver] + 1
                        })
                        driver_busy_times[driver].append((candidate_start_str, candidate_end_str))
                        driver_route_counts[driver] += 1
                        driver_worked_hours[driver] += worked_minutes / 60
                        placed = True
                        current_time = candidate_end_obj + timedelta(minutes=break_time + min_break_time)
                        break
                if not placed:
                    result = self.allocate_driver_to_route(actual_time, break_time, min_break_time, driver_list, driver_busy_times, driver_worked_hours, selected_day, driver_route_counts)
                    if result is None:
                        message = "Расписание не утверждено.\nДобавьте сотрудников или уменьшите количество рейсов."
                        messagebox.showerror("Ошибка", message)
                        return
                    else:
                        driver, slot_start = result
                        cend = self.calculate_route_completion(slot_start, actual_time)
                        worked_minutes = (datetime.strptime(cend, "%H:%M") - datetime.strptime(slot_start, "%H:%M")).seconds / 60
                        final_type = f"{route_type} (доп рейс)"
                        schedule.append({
                            'Водитель': driver,
                            'Тип маршрута': final_type,
                            'Время начала': slot_start,
                            'Время окончания': cend,
                            'Маршрутов за смену': driver_route_counts[driver] + 1
                        })
                        driver_busy_times[driver].append((slot_start, cend))
                        driver_worked_hours[driver] += worked_minutes / 60
        result_window = tb.Toplevel(parent_window)
        df = pd.DataFrame(schedule)
        if not df.empty:
            self.display_generated_timetable(result_window, df, "Итоговое расписание:")
        else:
            self.display_generated_timetable(result_window, pd.DataFrame(), "Расписание не сформировано.")
    
    def execute_genetic_algorithm(self, driver_list, shift_duration, num_routes, selected_day, generations=50, population_size=20, mutation_rate=0.1, break_time=10, min_break_time=30):
        population = []
        for _ in range(population_size):
            schedule, score = self.generate_genetic_schedule_attempt(driver_list, shift_duration, num_routes, selected_day, break_time, min_break_time)
            population.append({'schedule': schedule, 'fitness': self.assess_schedule_quality(schedule)})
        best_schedule = None
        best_fitness = -1
        for _ in range(generations):
            population = sorted(population, key=lambda x: x['fitness'], reverse=True)
            current_best = population[0]
            if current_best['fitness'] > best_fitness:
                best_fitness = current_best['fitness']
                best_schedule = current_best['schedule']
            if best_fitness >= num_routes:
                break
            parents = population[:population_size // 2]
            new_population = parents.copy()
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(parents, 2)
                child1_schedule, child2_schedule = self.execute_crossover(parent1['schedule'], parent2['schedule'])
                child1 = {'schedule': child1_schedule, 'fitness': self.assess_schedule_quality(child1_schedule)}
                child2 = {'schedule': child2_schedule, 'fitness': self.assess_schedule_quality(child2_schedule)}
                new_population.extend([child1, child2])
            for individual in new_population:
                if random.random() < mutation_rate:
                    mutated_schedule = self.execute_mutation(individual['schedule'], driver_list, break_time)
                    individual['schedule'] = mutated_schedule
                    individual['fitness'] = self.assess_schedule_quality(mutated_schedule)
            population = new_population[:population_size]
        result_window = tb.Toplevel(self.root)
        result_window.geometry("800x600")
        if best_fitness >= num_routes:
            title_text = "Генетический алгоритм завершен. Лучшее расписание"
        else:
            title_text = "Генетический алгоритм завершен. Лучшее найденное расписание"
        if best_schedule and best_fitness > 0:
            df = pd.DataFrame(best_schedule)
            self.display_generated_timetable(result_window, df, f"{title_text} ({best_fitness} рейсов):")
        else:
            self.display_generated_timetable(result_window, pd.DataFrame(), title_text)
    
    def start_genetic_schedule(self):
        try:
            num_routes = int(self.total_routes_entry.get())
            selected_day = self.selected_day_var.get()
            all_drivers = self.type_a_drivers + self.type_b_drivers
            shift_duration = max(self.shift_duration_a, self.shift_duration_b)
            additional_needed = self.calculate_additional_driver_needs(num_routes, all_drivers, shift_duration)
            if additional_needed > 0:
                message = f"Недостаточно водителей.\nДобавьте минимум {additional_needed} водителей или уменьшите количество рейсов."
                messagebox.showerror("Ошибка", message)
                return
            if not self.type_a_drivers and not self.type_b_drivers:
                messagebox.showerror("Ошибка", "Нет водителей.")
                return
            if self.is_weekend(selected_day) and not self.type_b_drivers:
                message = "Выходной: Тип A не работает, а типа B нет."
                messagebox.showerror("Ошибка", message)
                return
            if self.is_weekend(selected_day) and not self.type_a_drivers and self.type_b_drivers:
                additional_b = self.calculate_additional_driver_needs(num_routes, self.type_b_drivers, self.shift_duration_b)
                if additional_b > 0:
                    message = f"Недостаточно водителей B на выходной. Нужно {additional_b}."
                    messagebox.showerror("Ошибка", message)
                    return
            self.execute_genetic_algorithm(all_drivers, shift_duration, num_routes, selected_day, generations=50, population_size=20, mutation_rate=0.1, break_time=10, min_break_time=30)
        except ValueError:
            messagebox.showerror("Ошибка", "Не удалось сгенерировать: нужно добавить ещё водителей или уменьшить количество рейсов.")
    
    def start_schedule_creation(self):
        try:
            num_routes = int(self.total_routes_entry.get())
            selected_day = self.selected_day_var.get()
            all_drivers = self.type_a_drivers + self.type_b_drivers
            if not self.type_a_drivers and not self.type_b_drivers:
                messagebox.showerror("Ошибка", "Нет водителей.")
                return
            if self.is_weekend(selected_day) and not self.type_b_drivers:
                messagebox.showerror("Ошибка", "Выходной: Тип A не работает, а типа B нет.")
                return
            if self.is_weekend(selected_day) and not self.type_a_drivers and self.type_b_drivers:
                additional_b = self.calculate_additional_driver_needs(num_routes, self.type_b_drivers, self.shift_duration_b)
                if additional_b > 0:
                    message = f"Недостаточно водителей B на выходной. Нужно {additional_b}."
                    messagebox.showerror("Ошибка", message)
                    return
                self.build_optimized_timetable(self.type_b_drivers, self.shift_duration_b, num_routes, selected_day, self.root)
                return
            max_shift = max(self.shift_duration_a, self.shift_duration_b)
            self.build_optimized_timetable(all_drivers, max_shift, num_routes, selected_day, self.root)
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте введенные данные.")

if __name__ == "__main__":
    root = tb.Window(themename="cyborg")  # Выберите подходящую тему
    app = RouteScheduler(root)
    root.mainloop()
