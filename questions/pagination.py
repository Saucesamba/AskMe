import math

def get_fake_questions(cnt):
    return [ 
        {
        'id':i,
        'title': f'Title{i}',
        'question_text':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'tags':{
            'swag',
            'first',
            'tag',
        },
        'is_hot': False,
        'answer_count':3,
        'like_count': 52,
        } for i in range (1,cnt+1)
    ] 


def paginate(items, page, per_page = 10):
    size = len(items)
    max_page = math.ceil(size/per_page)
    max_buttons = 20

    half = max_buttons // 2
    start_page = max(1, page - half)
    end_page = min(max_page, start_page + max_buttons - 1)

    if end_page - start_page < max_buttons - 1:
        start_page = max(1, end_page - max_buttons + 1)

    visible_pages = [i for i in range(start_page, end_page + 1)]


    context = {
        'page':page,
        'questions_per_page':per_page,
        'count_questions':size,
        'max_page' : max_page,
        'pages' : visible_pages
    }

    start_index = (page - 1) * per_page
    end_index = page * per_page
    
    return context, items[start_index:end_index]
