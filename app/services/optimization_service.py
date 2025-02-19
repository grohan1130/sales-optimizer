import numpy as np
from decimal import Decimal

class OptimizationService:
    def __init__(self):
        pass

    def calculate_volume_at_price(self, price, best_guess_price, max_price, base_volume):
        """Calculate expected volume at a given price"""
        if price <= best_guess_price:
            return base_volume
        if price >= max_price:
            return 0
        
        # Linear interpolation
        volume_ratio = 1 - (price - best_guess_price) / (max_price - best_guess_price)
        return int(base_volume * volume_ratio)

    def optimize(self, monthly_volumes, cost, best_guess_price, max_price):
        """Find optimal price and calculate metrics"""
        
        # Convert to integers for price iteration
        cost = int(cost)
        best_guess_price = int(best_guess_price)
        max_price = int(max_price)
        
        best_profit = 0
        optimal_price = best_guess_price
        optimal_volumes = []
        optimal_revenue = 0
        
        # Try each possible integer price
        for price in range(best_guess_price, max_price + 1):
            current_volumes = []
            total_profit = 0
            total_revenue = 0
            
            # Calculate for each month
            for base_volume in monthly_volumes:
                volume = self.calculate_volume_at_price(price, best_guess_price, max_price, base_volume)
                revenue = price * volume
                profit = (price - cost) * volume
                
                total_profit += profit
                total_revenue += revenue
                current_volumes.append(volume)
            
            # Update optimal if better profit found
            if total_profit > best_profit:
                best_profit = total_profit
                optimal_price = price
                optimal_volumes = current_volumes
                optimal_revenue = total_revenue
        
        return {
            "optimal_price": optimal_price,
            "total_revenue": optimal_revenue,
            "total_profit": best_profit,
            "monthly_volumes": optimal_volumes
        } 