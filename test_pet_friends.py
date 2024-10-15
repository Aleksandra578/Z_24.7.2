from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api возвращает статус 200 и в результате содержит слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter_=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter_)
    assert status == 200
    assert len(result['pets']) > 0
    print(filter_)

def test_add_new_pet_with_valid_data(name='Марс', animal_type=',кот',
                                     age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Марс", "кот", "2", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Марсель', animal_type='котик', age=3):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_create_pet_simple_valid_data_without_photo(name='Барсик', animal_type='йорк', age='5'):
    """Проверяем что можно добавить питомца с корректными данными, без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age

def test_add_pet_photo_valid_data(pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавить фото питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['name'] == my_pets['pets'][0]['name']
        assert result['pet_photo'] != my_pets['pets'][0]['pet_photo']
    else:
        print("В списке питомцы отсутствуют")

# ==========================================================================================

def test_get_api_key_for_invalid_password_user(email=valid_email, password=invalid_password):
    """Проверяем возможность авторизации с корректным логином и некорректным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_email_user(email=invalid_email, password=valid_password):
    """Проверяем возможность авторизации с некорректным логином и корректным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем возможность авторизации с некорректным логином и некорректным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_with_invalid_name(name='1256871', animal_type='бульдог',
                                       age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными name"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_type(name='Марс', animal_type='15481623',
                                       age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными animal_type"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_age(name='Марс', animal_type='кот',
                                      age='-2', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными age"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age

def test_add_pets_set_photo_invalid(pet_photo='images/qaz.bmp'):
    """Проверяем возможность добавления фото питомца невалидного формата"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        # pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        print("В списке питомцы отсутствуют ")

def test_update_pet_info_invalid_type(name='Марсель', animal_type='//!!!ри5', age=2):
    """Проверяем возможность обновления информации о питомце с некорректной породой"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("В списке питомцы отсутствуют")

def test_update_self_pet_info_invalid_name(name='///!!!652', animal_type='йорк', age=5):
    """Проверяем возможность обновления информации о питомце с некорректным именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("В списке питомцы отсутствуют")

def test_update_pet_info_invalid_age(name='Масик', animal_type='котик', age=-1):
    """Проверяем возможность обновления информации о питомце с отрицательным возрастом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("В списке питомцы отсутствуют")