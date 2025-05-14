📦 Advanced OOP Inventory Management System (Python)
🎯 Objective
This project is a robust Inventory Management System built using Object-Oriented Programming (OOP) principles in Python.
It can manage different product types, handle stock operations, process sales, and persist data using JSON files.

This challenge is designed to polish your OOP concepts by applying them in a real-world scenario.

🛠 Features
1. Abstract Base Class: Product
Implemented using the abc module.

Encapsulated attributes:

_product_id

_name

_price

_quantity_in_stock

Abstract & concrete methods:

restock(amount)

sell(quantity)

get_total_value()

__str__()

2. Subclasses of Product
Electronics
Extra attributes: warranty_years, brand

Custom __str__() implementation

Grocery
Extra attribute: expiry_date

Method: is_expired()

Custom __str__() shows expiry status

Clothing
Extra attributes: size, material

Custom __str__() implementation

3. Class: Inventory
Manages a collection of Product instances.

Operations:

Add, remove, search, sell, restock products

Search by name or type

Calculate total inventory value

Remove expired groceries

Data persistence using JSON (save/load)

4. Bonus Features
Custom Exceptions:

DuplicateProductError
OutOfStockError
InvalidProductDataError
CLI Menu:

User-friendly interface to interact with inventory.

Options include adding, selling, viewing, saving, and loading products.

💾 Data Persistence
Save inventory to JSON file with full data.

Load inventory from JSON while correctly reconstructing the appropriate subclasses (Electronics, Grocery, Clothing).

💡 Concepts Demonstrated

✅ Abstraction (abc module)

✅ Inheritance & Polymorphism

✅ Encapsulation

✅ Custom exceptions and error handling

✅ JSON data persistence

✅ CLI interaction using while loop and user inputs



