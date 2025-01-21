import os
import pandas as pd
import sqlite3
from collections import Counter
import logging
import json

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analytics.log"),
        logging.StreamHandler()
    ]
)

# Создание логгера для вашего класса
logger = logging.getLogger(__name__)

class AnalyticsGenerator:
    def __init__(self):
        logger.info("Инициализация AnalyticsGenerator")
        # Директория для сохранения графиков
        self.output_dir = os.path.join(os.path.dirname(__file__), 'static', 'analytics')
        os.makedirs(self.output_dir, exist_ok=True)

        # Подключение к SQLite
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'vacancies.db'))
        self.curs = self.conn.cursor()
        logger.info("Соединение с базой данных установлено")

    def get_data_as_dataframe(self):
        """Получение данных из базы и преобразование в DataFrame."""
        logger.info("Получение данных из базы данных")
        query = '''SELECT name, key_skills, salary_from, salary_to, salary_in_rub, area, published_at, profession FROM Vacancy'''
        df = pd.read_sql_query(query, self.conn)
        logger.info("Данные успешно получены")
        return df

    def generate_chart_js_template(self, chart_type, data, labels, title, file_name):
        """Генерация HTML-файла с графиком Chart.js."""
        logger.info(f"Генерация графика {chart_type} для {file_name}")
        template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <canvas id="myChart" width="400" height="200"></canvas>
            <script>
                const ctx = document.getElementById('myChart').getContext('2d');
                const myChart = new Chart(ctx, {{
                    type: '{chart_type}',
                    data: {{
                        labels: {json.dumps(list(map(str, labels)))},
                        datasets: [{{
                            label: '{title}',
                            data: {json.dumps(list(map(str, data)))},
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """
        with open(os.path.join(self.output_dir, file_name), 'w', encoding='utf-8') as file:
            file.write(template)
        logger.info(f"График {chart_type} для {file_name} сгенерирован успешно")

    def generate_salary_trends(self):
        """Генерация графика динамики уровня зарплат по годам."""
        logger.info("Генерация трендов зарплат")
        df = self.get_data_as_dataframe()
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)
        df = df.dropna(subset=['published_at'])
        df['year'] = df['published_at'].dt.year
        salary_trends = df.groupby('year')['salary_in_rub'].mean().dropna()

        self.generate_chart_js_template(
            chart_type='line',
            data=salary_trends.tolist(),
            labels=salary_trends.index.tolist(),
            title='Динамика уровня зарплат по годам',
            file_name='salary_trends.html'
        )

    def generate_vacancy_count_trends(self):
        """Генерация графика динамики количества вакансий по годам."""
        logger.info("Генерация трендов количества вакансий")
        df = self.get_data_as_dataframe()
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)
        df = df.dropna(subset=['published_at'])
        df['year'] = df['published_at'].dt.year
        vacancy_counts = df['year'].value_counts().sort_index()

        self.generate_chart_js_template(
            chart_type='bar',
            data=vacancy_counts.tolist(),
            labels=vacancy_counts.index.tolist(),
            title='Динамика количества вакансий по годам',
            file_name='vacancy_count_trends.html'
        )

    def generate_salary_by_city(self):
        """Генерация графика зарплат по городам."""
        logger.info("Генерация зарплат по городам")
        df = self.get_data_as_dataframe()
        salary_by_city = df.groupby('area')['salary_in_rub'].mean().sort_values(ascending=False).head(10)

        self.generate_chart_js_template(
            chart_type='bar',
            data=salary_by_city.tolist(),
            labels=salary_by_city.index.tolist(),
            title='Средняя зарплата по городам',
            file_name='salary_by_city.html'
        )

    def generate_city_vacancy_share(self):
        """Генерация графика доли вакансий по городам."""
        logger.info("Генерация доли вакансий по городам")
        df = self.get_data_as_dataframe()
        city_vacancy_share = df['area'].value_counts(normalize=True).head(10) * 100

        self.generate_chart_js_template(
            chart_type='pie',
            data=city_vacancy_share.tolist(),
            labels=city_vacancy_share.index.tolist(),
            title='Доля вакансий по городам',
            file_name='city_vacancy_share.html'
        )

    def generate_skill_frequency(self):
        """Генерация графика топ-20 навыков."""
        logger.info("Генерация частоты навыков")
        df = self.get_data_as_dataframe()
        skills = df['key_skills'].dropna().str.split(',').explode()
        top_skills = Counter(skills).most_common(20)

        skill_names, skill_counts = zip(*top_skills)
        self.generate_chart_js_template(
            chart_type='bar',
            data=list(skill_counts),
            labels=list(skill_names),
            title='ТОП-20 навыков',
            file_name='top_skills.html'
        )

    def generate_salary_trends_for_profession(self):
        """Генерация графика уровня зарплат по годам для профессии 'Разработчик игр (GameDev)'."""
        logger.info("Генерация трендов зарплат для профессии 'Разработчик игр (GameDev)'")
        df = self.get_data_as_dataframe()
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)
        df = df.dropna(subset=['published_at'])
        df['year'] = df['published_at'].dt.year

        # Ключевые слова для поиска профессии
        keywords = ['game', 'unity', 'игр', 'unreal']

        # Фильтрация вакансий по ключевым словам в названии и скиллах
        profession_df = df[df.apply(lambda row: any(keyword in row['name'].lower() for keyword in keywords) or any(keyword in row['key_skills'].lower() for keyword in keywords), axis=1)]

        salary_trends = profession_df.groupby('year')['salary_in_rub'].mean().dropna()

        if not salary_trends.empty:
            self.generate_chart_js_template(
                chart_type='line',
                data=salary_trends.tolist(),
                labels=salary_trends.index.tolist(),
                title='Динамика уровня зарплат для Разработчик игр (GameDev)',
                file_name='salary_trends_GameDev.html'
            )
        else:
            logger.warning("Нет данных для генерации трендов зарплат для профессии 'Разработчик игр (GameDev)'")

    def generate_vacancy_count_for_profession(self):
        """Генерация графика количества вакансий по годам для профессии 'Разработчик игр (GameDev)'."""
        logger.info("Генерация количества вакансий для профессии 'Разработчик игр (GameDev)'")
        df = self.get_data_as_dataframe()
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)
        df = df.dropna(subset=['published_at'])
        df['year'] = df['published_at'].dt.year

        # Ключевые слова для поиска профессии
        keywords = ['game', 'unity', 'игр', 'unreal']

        # Фильтрация вакансий по ключевым словам в названии и скиллах
        profession_df = df[df.apply(lambda row: any(keyword in row['name'].lower() for keyword in keywords) or any(keyword in row['key_skills'].lower() for keyword in keywords), axis=1)]

        vacancy_counts = profession_df['year'].value_counts().sort_index()

        if not vacancy_counts.empty:
            self.generate_chart_js_template(
                chart_type='bar',
                data=vacancy_counts.tolist(),
                labels=vacancy_counts.index.tolist(),
                title='Количество вакансий для Разработчик игр (GameDev) по годам',
                file_name='vacancy_count_GameDev.html'
            )
        else:
            logger.warning("Нет данных для генерации количества вакансий для профессии 'Разработчик игр (GameDev)'")

    def generate_salary_by_city_for_profession(self):
        """Генерация графика уровня зарплат по городам для выбранной профессии."""
        logger.info("Генерация уровня зарплат по городам для выбранной профессии")
        df = self.get_data_as_dataframe()

        # Ключевые слова для поиска профессии
        keywords = ['game', 'unity', 'игр', 'unreal']

        # Фильтрация вакансий по ключевым словам в названии и скиллах
        profession_df = df[df.apply(lambda row: any(keyword in row['name'].lower() for keyword in keywords) or any(keyword in row['key_skills'].lower() for keyword in keywords), axis=1)]

        salary_by_city = profession_df.groupby('area')['salary_in_rub'].mean().sort_values(ascending=False).head(10)

        if not salary_by_city.empty:
            self.generate_chart_js_template(
                chart_type='bar',
                data=salary_by_city.tolist(),
                labels=salary_by_city.index.tolist(),
                title='Уровень зарплат по городам для Разработчик игр (GameDev)',
                file_name='salary_by_city_GameDev.html'
            )
        else:
            logger.warning("Нет данных для генерации уровня зарплат по городам для профессии 'Разработчик игр (GameDev)'")

    def generate_city_vacancy_share_for_profession(self):
        """Генерация графика доли вакансий по городам для выбранной профессии."""
        logger.info("Генерация доли вакансий по городам для выбранной профессии")
        df = self.get_data_as_dataframe()

        # Ключевые слова для поиска профессии
        keywords = ['game', 'unity', 'игр', 'unreal']

        # Фильтрация вакансий по ключевым словам в названии и скиллах
        profession_df = df[df.apply(lambda row: any(keyword in row['name'].lower() for keyword in keywords) or any(keyword in row['key_skills'].lower() for keyword in keywords), axis=1)]

        city_vacancy_share = profession_df['area'].value_counts(normalize=True).head(10) * 100

        if not city_vacancy_share.empty:
            self.generate_chart_js_template(
                chart_type='pie',
                data=city_vacancy_share.tolist(),
                labels=city_vacancy_share.index.tolist(),
                title='Доля вакансий по городам для Разработчик игр (GameDev)',
                file_name='city_vacancy_share_GameDev.html'
            )
        else:
            logger.warning("Нет данных для генерации доли вакансий по городам для профессии 'Разработчик игр (GameDev)'")

    def generate_top_skills_by_year_for_profession(self):
        """Генерация графика самых популярных навыков по годам для выбранной профессии."""
        logger.info("Генерация самых популярных навыков по годам для выбранной профессии")
        df = self.get_data_as_dataframe()
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)
        df = df.dropna(subset=['published_at'])
        df['year'] = df['published_at'].dt.year

        # Ключевые слова для поиска профессии
        keywords = ['game', 'unity', 'игр', 'unreal']

        # Фильтрация вакансий по ключевым словам в названии и скиллах
        profession_df = df[df.apply(lambda row: any(keyword in row['name'].lower() for keyword in keywords) or any(
            keyword in row['key_skills'].lower() for keyword in keywords), axis=1)]

        # Разбиение колонки key_skills на отдельные навыки
        profession_df.loc[:, 'key_skills'] = profession_df['key_skills'].str.split(',')
        profession_df = profession_df.explode('key_skills')

        top_skills_by_year = {}
        for year in profession_df['year'].unique():
            year_df = profession_df[profession_df['year'] == year]
            top_skill = Counter(year_df['key_skills'].dropna()).most_common(1)
            if top_skill:
                top_skills_by_year[year] = top_skill[0]

        if top_skills_by_year:
            labels = [f"{skill} ({year})" for year, (skill, count) in top_skills_by_year.items()]
            data = [count for year, (skill, count) in top_skills_by_year.items()]
            self.generate_chart_js_template(
                chart_type='bar',
                data=data,
                labels=labels,
                title='Самые популярные навыки по годам для Разработчик игр (GameDev)',
                file_name='top_skills_by_year_GameDev.html'
            )
        else:
            logger.warning(
                "Нет данных для генерации самых популярных навыков по годам для профессии 'Разработчик игр (GameDev)'")

    def generate_all(self):
        """Генерация всех графиков."""
        logger.info("Генерация всех графиков")
        self.generate_salary_trends()
        self.generate_vacancy_count_trends()
        self.generate_salary_by_city()
        self.generate_city_vacancy_share()
        self.generate_skill_frequency()
        self.generate_salary_trends_for_profession()
        self.generate_vacancy_count_for_profession()
        self.generate_salary_by_city_for_profession()
        self.generate_city_vacancy_share_for_profession()
        self.generate_top_skills_by_year_for_profession()
        logger.info("Все графики сгенерированы успешно")

if __name__ == "__main__":
    logger.info("Начало выполнения скрипта")
    analytics = AnalyticsGenerator()
    analytics.generate_all()
    logger.info("Скрипт выполнен успешно")
