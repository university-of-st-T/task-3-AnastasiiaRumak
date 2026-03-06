def add_ingredient(inventory, ingredient, amount):
    """
    Добавляет ingredient в количестве amount в inventory.
    Если ингредиент уже есть, его количество увеличивается;
    иначе создаётся новая запись.
    """
    inventory[ingredient] = inventory.get(ingredient, 0) + amount


def brew_potion(inventory, recipes, potion_name):
    """
    Пытается приготовить зелье с именем potion_name.
    Возвращает True, если удалось (ингредиенты вычтены),
    иначе False (инвентарь остаётся без изменений).
    """
    # 1. Проверяем, есть ли такой рецепт
    if potion_name not in recipes:
        return False

    recipe = recipes[potion_name]

    # 2. Проверяем наличие всех ингредиентов в нужном количестве
    for ingredient, needed in recipe.items():
        if inventory.get(ingredient, 0) < needed:
            return False

    # 3. Если всё в порядке – вычитаем ингредиенты
    for ingredient, needed in recipe.items():
        inventory[ingredient] -= needed
        # Если количество стало равно нулю, удаляем запись
        if inventory[ingredient] == 0:
            del inventory[ingredient]

    return True
