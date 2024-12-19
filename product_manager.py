class ProductManager:
    def __init__(self, product_file):
        self.product_file = product_file

    def add_product(self, username, product, quantity, price):
        with open(self.product_file, mode='a') as file:
            file.write(f"{username}, {product},{quantity},{price}\n")

    def display_list(self, username):
        try:
            with open(self.product_file, 'r') as file:
                products = [line.strip().split(',') for line in file if line.startswith(username + ",")]

            if products:
                print("\nVotre liste de produits :")
                print(f"{'Produit':<20} {'Quantité':<10} {'Prix unitaire':<15}")
                for product in products:
                    print(f"{product[1]:<20} {product[2]:<10} {product[3]:<15}")
            else:
                print("Aucun produit trouvé dans votre liste.")
        except FileNotFoundError:
            print("Le fichier de produits est introuvable.")

    def sort_by_quantity(self):
        with open(self.product_file, 'r') as file:
            lines = file.readlines()
        for i in range(1, len(lines)):
            current_line = lines[i]
            current_quantity = float(current_line.strip().split(',')[2])
            j = i - 1

            while j >= 0 and float(lines[j].strip().split(',')[2]) > current_quantity:
                lines[j + 1] = lines[j]
                j -= 1

            lines[j + 1] = current_line

        with open(self.product_file, 'w') as file:
            for line in lines:
                file.write(line.strip() + '\n')

        print("Le tri par quantité a été effectué.")

    def quicksort_by_price(self, lines):
        if len(lines) <= 1:
            return lines
        pivot = float(lines[-1].strip().split(',')[3])

        less_than_pivot = [line for line in lines[:-1] if float(line.strip().split(',')[3]) <= pivot]
        greater_than_pivot = [line for line in lines[:-1] if float(line.strip().split(',')[3]) > pivot]

        return self.quicksort_by_price(less_than_pivot) + [lines[-1]] + self.quicksort_by_price(greater_than_pivot)

    def sort_by_price(self):
        with open(self.product_file, 'r') as file:
            lines = file.readlines()

        sorted_lines = self.quicksort_by_price(lines)
        with open(self.product_file, 'w') as file:
            for line in sorted_lines:
                file.write(line.strip() + '\n')

        print("Le tri par prix avec QuickSort a été effectué.")
