import pytest
from alchemy import add_ingredient, brew_potion

# Тесты для add_ingredient
def test_add_ingredient_new():
    inventory = {}
    add_ingredient(inventory, "herb", 5)
    assert inventory == {"herb": 5}

def test_add_ingredient_existing():
    inventory = {"herb": 3}
    add_ingredient(inventory, "herb", 2)
    assert inventory == {"herb": 5}

def test_add_ingredient_multiple():
    inventory = {}
    add_ingredient(inventory, "herb", 5)
    add_ingredient(inventory, "water", 3)
    add_ingredient(inventory, "herb", 2)
    assert inventory == {"herb": 7, "water": 3}

# Фикстура с рецептами для тестов brew_potion
@pytest.fixture
def recipes():
    return {
        "health_potion": {"herb": 2, "water": 1},
        "mana_potion": {"crystal": 1, "water": 2},
        "invisibility_potion": {"mushroom": 3, "water": 2, "herb": 1}
    }

# Тесты для brew_potion
def test_brew_potion_success(recipes):
    inventory = {"herb": 5, "water": 3, "crystal": 1}
    result = brew_potion(inventory, recipes, "health_potion")
    assert result == True
    assert inventory == {"herb": 3, "water": 2, "crystal": 1}

def test_brew_potion_remove_zero(recipes):
    inventory = {"herb": 2, "water": 1, "crystal": 1}
    result = brew_potion(inventory, recipes, "health_potion")
    assert result == True
    # herb и water должны стать 0 и удалиться
    assert inventory == {"crystal": 1}

def test_brew_potion_insufficient(recipes):
    inventory = {"herb": 1, "water": 1, "crystal": 1}  # не хватает herb
    result = brew_potion(inventory, recipes, "health_potion")
    assert result == False
    assert inventory == {"herb": 1, "water": 1, "crystal": 1}  # без изменений

def test_brew_potion_missing_ingredient(recipes):
    inventory = {"water": 1, "crystal": 1}  # нет herb
    result = brew_potion(inventory, recipes, "health_potion")
    assert result == False
    assert inventory == {"water": 1, "crystal": 1}

def test_brew_potion_unknown_potion(recipes):
    inventory = {"herb": 5}
    result = brew_potion(inventory, recipes, "love_potion")
    assert result == False
    assert inventory == {"herb": 5}

def test_brew_potion_multiple_success(recipes):
    inventory = {"herb": 5, "water": 5, "crystal": 2, "mushroom": 3}
    # Варим invisibility_potion
    result1 = brew_potion(inventory, recipes, "invisibility_potion")
    assert result1 == True
    assert inventory == {"herb": 4, "water": 3, "crystal": 2}
    assert "mushroom" not in inventory  # должен удалиться

    # Варим mana_potion
    result2 = brew_potion(inventory, recipes, "mana_potion")
    assert result2 == True
    assert inventory == {"herb": 4, "water": 1, "crystal": 1}

    # Варим health_potion
    result3 = brew_potion(inventory, recipes, "health_potion")
    assert result3 == True
    assert inventory == {"herb": 2, "crystal": 1}
    assert "water" not in inventory
