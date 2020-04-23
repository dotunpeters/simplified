
#convert paginated object into list of dictionary object
def parser(render):
    products = []
    products.append({'success': True})
    for each in render.items:
        dict_each = {}
        dict_each["name"] = each.name
        dict_each["sku"] = each.sku
        dict_each["price"] = each.price
        dict_each["stars"] = each.stars
        dict_each["original"] = int(float(each.stars) * 20)
        dict_each["link"] = each.link
        dict_each["image_url"] = each.image_url
        dict_each["reviews"] = each.reviews
        dict_each["seller"] = each.seller
        dict_each["category"] = each.category
        dict_each["description"] = each.description
        products.append(dict_each)
    return products