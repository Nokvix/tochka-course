import uvicorn
import os
from fastapi import FastAPI
from app.models import Post, PostUpdate
from app.utils import dict_list_to_json, json_to_dict_list
from typing import List, Dict


path_to_file = os.path.join(os.getcwd(), 'posts.json')
app = FastAPI()


@app.get('/posts')
def get_posts(index: int | None = None, category: int | None = None) -> List[Post]:
    posts = json_to_dict_list(path_to_file)

    if index:
        posts = [post for post in posts if post.get('id') == index]

    if category:
        posts = [post for post in posts if post.get('category') == category]

    return posts


@app.post('/add_post', status_code=201)
def add_post(post: Post):
    posts = json_to_dict_list(path_to_file)
    post_dict = post.dict()
    posts.append(post_dict)
    dict_list_to_json(posts, path_to_file)


@app.patch('/update_post', status_code=200)
def update_post(post_update: PostUpdate, index: int | None = None):
    if not index:
        return {'message': 'Выберите пост, который нужно изменить'}

    posts = json_to_dict_list(path_to_file)
    for i, post in enumerate(posts):
        if post.get('id') == index:
            posts[i] = {**posts[i], **post_update.dict(exclude_unset=True)}
            dict_list_to_json(posts, path_to_file)
            return {'message': 'Пост обновлен'}

    return {'message': 'Пост не найден'}


@app.delete('/delete_post', status_code=200)
def delete_post(index: int | None = None):
    if not index:
        return {'message': 'Выберите пост, который хотите удалить'}

    posts = json_to_dict_list(path_to_file)
    len_posts = len(posts)

    posts = [post for post in posts if post.get('id') != index]
    if len_posts == len(posts):
        return {'message': 'Пост не найден'}

    dict_list_to_json(posts, path_to_file)
    return {'message': 'Пост удалён'}


