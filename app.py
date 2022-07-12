# Подключаем все необходимые модули
from database import session
from table_user import User
from table_post import Post
from typing import List
from fastapi import FastAPI
from schema import PostGet
from datetime import datetime
import pandas as pd
import os
from catboost import CatBoostClassifier

app = FastAPI()
# Читаем данные из БД из таблицы post_text_df для сбора признаков
post_query = session.query(Post.post_id, Post.text, Post.topic).all()
post_df = pd.DataFrame(post_query)
app = FastAPI()
# Читаем данные из БД из таблицы user_data для сбора признаков
user_query = session.query(User.user_id, User.gender, User.city,
                          User.exp_group, User.os,User.country,
                          User.source, User.age).all()
user_df = pd.DataFrame(user_query)

def get_model_path(path: str) -> str:
    """Получаем путь к файлу модельки"""

    MODEL_PATH = "/home/user/Karpov Courses StartML/catboost_model"
    return MODEL_PATH


def load_models():
    """Загрузка заранее сохраненной модели МО"""

    model_path = get_model_path(os.environ)
    from_file = CatBoostClassifier()
    model = from_file.load_model(model_path)

    return model

def load_features(id: int)--> pd.DataFrame:
    """Подтягиваем все фичи в один датафрейм
    по конкретному пользователю"""

    ordered_columns = ['post_id', 'user_id', 'gender', 'age', 'country', 'city', 'exp_group',
       'os', 'source', 'text', 'topic']

    all_features_df = user_df.loc[user_df.user_id == id].merge(post_df, how='cross')
    # Выстраиваем тот же порядок колонок что и был при обучении модели
    all_features_df = all_features_df[ordered_columns]

    return all_features_df


loaded_catboost = load_models()

@app.get("/post/recommendations/", response_model=List[PostGet])
async def get_post_rec(id: int, time: datetime, limit: int):
"""Endpoint для предсказания топ рекоммендаций в социальной сети
по 1 введенному пользователю"""

    total_df = load_features(id)
    total_df['year'] = time.year
    total_df['month'] = time.month
    total_df['day'] = time.day
    total_df['hour'] = time.hour
    total_df['preds_proba'] = loaded_catboost.predict_proba(total_df)[:,1]
    total_df.rename(columns = {"post_id": "id"}, inplace = True)
    total_df = total_df.sort_values('preds_proba', ascending=False)[['id', 'text', 'topic']].head(limit)

    return total_df.to_dict(orient='records')
