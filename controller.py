from restDataAccess import Model

NAME = 'name'
ADDRESS = 'address'
CITY = 'city'
STATE = 'state'
ZIPCODE = 'zip_code'
VEGETARIAN = 'vegetarian'
VEGAN = 'vegan'
GLUTEN = 'gluten'
MENU = 'menu'
HOURS = 'hours'
DESCRIPTION = 'description'

model = Model()


def add_new_resturant(
        name='',
        address='',
        city='',
        state='',
        zip_code='',
        vegetarian='',
        vegan='',
        gluten='',
        menu='',
        hours='',
        description=''):
    restaurant_dict = {
        NAME: name,
        ADDRESS: address,
        CITY: city,
        STATE: state,
        ZIPCODE: zip_code,
        VEGETARIAN: vegetarian,
        VEGAN: vegan,
        GLUTEN: gluten,
        MENU: menu,
        HOURS: hours,
        DESCRIPTION: description
    }

    model.insert_restaurant(restaurant_dict)

def get_restaurant_by_id(id):
    rest = model.select_rest_by_id(id)
    if(rest=None):
        print("Id doesnt exist")
    return rest


def get_restaurants_by_att(restaurant_dict, sort_by=None, assending=False):
    return model.select_rest_by_attribute(restaurant_dict, sort_by, assending)





if __name__ == "__main__":
    get_restaurant(id)
