predefined_urls = {
            '/about' : '/home/about',
            '/cart' : '/shop/cart'
        } 

def parse_path(path:str) -> dict:
    # перевіряємо скорочені адреси
    path = predefined_urls.get(path, path)
    # розбираємо запит за принципом /controller/action
    parts = path.split('/') # запит починаємо з '/', 0-й ігноруємо
        # запит               parts
        # /                   ['','']
        # /controller         ['','controller']
        # /controller/        ['','controller','']
        # /ctrl/act           ['','ctrl','act']
        # /ctrl/act/          ['','ctrl','act','']
    return {
        "controller" : (parts[1].capitalize() if parts[1] != '' else 'Home')+"Controller",
        "action" : parts[2] if len(parts) > 2 and parts[2] != '' else 'index',
        "lang":"uk",
        "path-id": None
    }