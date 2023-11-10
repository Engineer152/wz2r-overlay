import requests

# example = {'camoId': 'mwii', 'title': 'MW2 Multiplayer', 'imageUrlUser': 'https://assets.codmunity.gg/profiles/135f77d1-7c47-11ee-ac49-4f8d923a28fa.webp', 'imageUrlMasteryCamo': 'https://assets.codmunity.gg/images/camo4.png', 'username': 'legend79', 'displayName': 'Legend79', 'camos': [{'title': 'Gold', 'progress': 32, 'total': 77}, {'title': 'Platinium', 'progress': 25, 'total': 77}, {'title': 'Polyatomic', 'progress': 0, 'total': 77}, {'title': 'ORION', 'progress': 0, 'total': 51}]}

default = {'camoId': 'none', 'title': 'N/A', 'imageUrlUser': 'https://static-cdn.jtvnw.net/user-default-pictures-uv/13e5fa74-defa-11e9-809c-784f43822e80-profile_image-150x150.png', 'imageUrlMasteryCamo': '', 'username': 'none', 'displayName': 'N/A', 'camos': [{'title': 'N/A', 'progress': 0, 'total': 0}, {'title': 'N/A', 'progress': 0, 'total': 0}, {'title': 'N/A', 'progress': 0, 'total': 0}, {'title': 'N/A', 'progress': 0, 'total': 0}]}

def get_camo_stats(typeofcamo="none",username="none"):
    url = f"https://api.codmunity.gg/users/camo/{typeofcamo}/{username}"
    try: r = requests.get(url,timeout=10)
    except: return default
    try: data = r.json()
    except: return default
    if "username" not in data.keys():
        return default  
    # Camo Titles
    camos = data['camos']
    camnew = []
    for c in camos:
        c['title'] = c['title'].upper()
        if c['progress'] == "":
            c['progress']="0"
        camnew.append(c)
    data['camos'] = camnew
    return data