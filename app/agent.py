"""Order processing agent for NoPickles MVP"""

import re
from typing import Dict, List
from app.models import Order, OrderItem
from app.menu import find_item_by_name, get_menu_items, get_recommendations, MENU_BY_CATEGORY


class OrderAgent:
    """Simple conversational agent for processing orders"""
    
    def __init__(self):
        self.context = []
    
    def process_message(self, message: str, order: Order) -> Dict:
        """Process a customer message and update the order"""
        message_lower = message.lower().strip()
        
        # Track conversation context
        self.context.append(message_lower)
        
        # Intent detection
        if self._is_greeting(message_lower):
            return self._handle_greeting()
        
        elif self._is_menu_request(message_lower):
            return self._handle_menu_request(message_lower)
        
        elif self._is_add_item(message_lower):
            return self._handle_add_item(message_lower, order)
        
        elif self._is_remove_item(message_lower):
            return self._handle_remove_item(message_lower, order)
        
        elif self._is_complete_order(message_lower):
            return self._handle_complete_order(order)
        
        elif self._is_help_request(message_lower):
            return self._handle_help()
        
        else:
            # Try to interpret as an item request
            result = self._handle_add_item(message_lower, order)
            if "added" in result["message"].lower():
                return result
            else:
                return {
                    "message": "I'm not sure what you mean. Try saying 'I want a burger' or 'show me the menu'.",
                    "suggestions": []
                }
    
    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        return any(greeting in message for greeting in greetings)
    
    def _is_menu_request(self, message: str) -> bool:
        """Check if user is asking for the menu"""
        keywords = ["menu", "what do you have", "what's available", "show me", "options"]
        return any(keyword in message for keyword in keywords)
    
    def _is_add_item(self, message: str) -> bool:
        """Check if user wants to add an item"""
        add_keywords = ["want", "get", "add", "order", "i'll have", "give me", "can i get"]
        return any(keyword in message for keyword in add_keywords)
    
    def _is_remove_item(self, message: str) -> bool:
        """Check if user wants to remove an item"""
        remove_keywords = ["remove", "delete", "cancel", "take off", "no"]
        return any(keyword in message for keyword in remove_keywords)
    
    def _is_complete_order(self, message: str) -> bool:
        """Check if user wants to complete the order"""
        complete_keywords = ["done", "complete", "finish", "checkout", "that's all", "that's it"]
        return any(keyword in message for keyword in complete_keywords)
    
    def _is_help_request(self, message: str) -> bool:
        """Check if user is asking for help"""
        return "help" in message or "how" in message
    
    def _handle_greeting(self) -> Dict:
        """Handle greeting messages"""
        return {
            "message": "Hello! Welcome to NoPickles. What can I get for you today?",
            "suggestions": ["Show me the menu", "I want a burger"]
        }
    
    def _handle_menu_request(self, message: str) -> Dict:
        """Handle menu information requests"""
        # Check if asking for specific category
        if "burger" in message:
            items = MENU_BY_CATEGORY.get("burgers", [])
            item_list = ", ".join([f"{item.name} (${item.price})" for item in items])
            return {
                "message": f"Our burgers: {item_list}",
                "suggestions": []
            }
        elif "drink" in message or "beverage" in message:
            items = MENU_BY_CATEGORY.get("drinks", [])
            item_list = ", ".join([f"{item.name} (${item.price})" for item in items])
            return {
                "message": f"Our drinks: {item_list}",
                "suggestions": []
            }
        elif "side" in message or "fries" in message:
            items = MENU_BY_CATEGORY.get("sides", [])
            item_list = ", ".join([f"{item.name} (${item.price})" for item in items])
            return {
                "message": f"Our sides: {item_list}",
                "suggestions": []
            }
        else:
            return {
                "message": "We have burgers, sides, drinks, and desserts. What would you like to know about?",
                "suggestions": ["Show me burgers", "What drinks do you have?"]
            }
    
    def _handle_add_item(self, message: str, order: Order) -> Dict:
        """Handle adding items to the order"""
        # Extract potential item names from message
        menu_item = find_item_by_name(message)
        
        if menu_item:
            # Check if item already in order
            existing_item = None
            for item in order.items:
                if item.menu_item_id == menu_item.id:
                    existing_item = item
                    break
            
            if existing_item:
                existing_item.quantity += 1
                order.total += menu_item.price
                response_msg = f"Added another {menu_item.name}. You now have {existing_item.quantity}."
            else:
                new_item = OrderItem(
                    menu_item_id=menu_item.id,
                    name=menu_item.name,
                    quantity=1,
                    price=menu_item.price
                )
                order.items.append(new_item)
                order.total += menu_item.price
                response_msg = f"Added {menu_item.name} (${menu_item.price}) to your order."
            
            # Get smart recommendations
            suggestions = get_recommendations(order.items)
            
            return {
                "message": response_msg,
                "suggestions": suggestions
            }
        else:
            return {
                "message": "I couldn't find that item on our menu. Could you try again or ask to see the menu?",
                "suggestions": ["Show me the menu"]
            }
    
    def _handle_remove_item(self, message: str, order: Order) -> Dict:
        """Handle removing items from the order"""
        if not order.items:
            return {
                "message": "Your order is already empty.",
                "suggestions": ["Show me the menu"]
            }
        
        # Try to find item to remove
        menu_item = find_item_by_name(message)
        
        if menu_item:
            for i, item in enumerate(order.items):
                if item.menu_item_id == menu_item.id:
                    if item.quantity > 1:
                        item.quantity -= 1
                        order.total -= item.price
                        return {
                            "message": f"Removed one {item.name}. You now have {item.quantity}.",
                            "suggestions": []
                        }
                    else:
                        order.items.pop(i)
                        order.total -= item.price
                        return {
                            "message": f"Removed {item.name} from your order.",
                            "suggestions": []
                        }
            
            return {
                "message": f"{menu_item.name} is not in your order.",
                "suggestions": []
            }
        else:
            # Remove last item as fallback
            removed = order.items.pop()
            order.total -= removed.price * removed.quantity
            return {
                "message": f"Removed {removed.name} from your order.",
                "suggestions": []
            }
    
    def _handle_complete_order(self, order: Order) -> Dict:
        """Handle order completion"""
        if not order.items:
            return {
                "message": "Your order is empty. Would you like to add something?",
                "suggestions": ["Show me the menu"]
            }
        
        items_summary = ", ".join([f"{item.quantity}x {item.name}" for item in order.items])
        return {
            "message": f"Great! Your order: {items_summary}. Total: ${order.total:.2f}. Ready to complete?",
            "suggestions": ["Yes, complete it", "Add more items"]
        }
    
    def _handle_help(self) -> Dict:
        """Handle help requests"""
        return {
            "message": "You can say things like: 'I want a burger', 'Add fries', 'Show me the menu', 'Remove the salad', or 'Complete my order'.",
            "suggestions": ["Show me the menu", "I want a burger"]
        }
