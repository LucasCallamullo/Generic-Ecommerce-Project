from django.db import models

# Create your models here.


from users.models import CustomUser
from productos.models import Product
from django.db import transaction


class Cart(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name="carrito")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def update_cart_db(self, product, action='nada', qty=0):
        """
        Centraliza todas las actualizaciones del carrito con un método en el mismo modelo.
        Para asegurar la consistencia de la base de datos, se utiliza el método atomic().

        Args:
            product (Product): El producto que se está agregando, eliminando o modificando en el carrito.
            action (str, optional): La acción a realizar. Los valores posibles son:
                - 'add': Agregar el producto al carrito.
                - 'remove': Eliminar el producto del carrito.
                - 'substract': Restar la cantidad del producto en el carrito.
                Por defecto es 'nada', lo que no realiza ninguna acción.
            qty (int, optional): La cantidad a agregar o restar. El valor predeterminado es 0.

        Returns:
            None
        """
        with transaction.atomic():
            if action == 'add':
                cart_item, created = self.items.get_or_create(product=product)
                cart_item.quantity = qty
                cart_item.save()
            
            elif action == 'remove':
                self.items.filter(product=product).delete()
            
            elif action == 'substract':
                cart_item = self.items.filter(product=product).first()
                
                if cart_item.quantity > 1:
                    cart_item.quantity -= qty
                    cart_item.save()
                else:
                    cart_item.delete()



class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("productos.Product", on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)
    
    class Meta:
        indexes = [
            models.Index(fields=['cart', 'product']),
        ]
