import requests

# example = {'camoId': 'mwii', 'title': 'MW2 Multiplayer', 'imageUrlUser': 'https://assets.codmunity.gg/profiles/135f77d1-7c47-11ee-ac49-4f8d923a28fa.webp', 'imageUrlMasteryCamo': 'https://assets.codmunity.gg/images/camo4.png', 'username': 'legend79', 'displayName': 'Legend79', 'camos': [{'title': 'Gold', 'progress': 32, 'total': 77}, {'title': 'Platinium', 'progress': 25, 'total': 77}, {'title': 'Polyatomic', 'progress': 0, 'total': 77}, {'title': 'ORION', 'progress': 0, 'total': 51}]}

default = {'camoId': 'none', 'title': 'N/A', 'imageUrlUser': 'https://static-cdn.jtvnw.net/user-default-pictures-uv/13e5fa74-defa-11e9-809c-784f43822e80-profile_image-150x150.png', 'imageUrlMasteryCamo': '', 'username': 'none', 'displayName': 'N/A', 'camos': [{'title': 'N/A', 'progress': 0, 'total': 0}, {'title': 'N/A', 'progress': 0, 'total': 0}, {'title': 'N/A', 'progress': 0, 'total': 0}, {'title': 'N/A', 'progress': 0, 'total': 0}]}

def default_data(typeofcamo,username):
    default['camoId']=typeofcamo
    default['username']=username
    return default

def get_camo_stats(typeofcamo="none",username="none"):
    url = f"https://api.codmunity.gg/users/camo/{typeofcamo}/{username}"
    try: r = requests.get(url,timeout=10)
    except: return default_data(typeofcamo,username)
    try: data = r.json()
    except: return default_data(typeofcamo,username)
    if "username" not in data.keys():
        return default_data(typeofcamo,username) 
    # Camo Titles
    camos = data['camos']
    camnew = []
    for c in camos:
        c['title'] = c['title'].upper()
        if c['progress'] == "":
            c['progress']="0"
        camnew.append(c)
    data['camos'] = camnew
    if "imageUrlUser" not in data:
        data["imageUrlUser"] = "https://static-cdn.jtvnw.net/user-default-pictures-uv/13e5fa74-defa-11e9-809c-784f43822e80-profile_image-150x150.png"
    return data

def get_new_camo_stats(typeofcamo="none",username="none"):
    url = f"https://api.codmunity.gg/users/camo/{typeofcamo}/{username}"
    r = requests.get(url,timeout=10)
    data = r.json()
    camos = data['camos']
    camnew = []
    for c in camos:
        c['title'] = c['title'].upper()
        if c['progress'] == "":
            c['progress']="0"
        camnew.append(c)
    data['camos'] = camnew
    if "imageUrlUser" not in data:
        data["imageUrlUser"] = "https://static-cdn.jtvnw.net/user-default-pictures-uv/13e5fa74-defa-11e9-809c-784f43822e80-profile_image-150x150.png"
    return data