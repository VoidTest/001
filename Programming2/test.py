import pygame
import json
import os


class Resource:
    def __init__(self, name, amount=0, rate=0):
        self.name = name
        self.amount = amount
        self.rate = rate

    def generate(self, delta_time):
        self.amount += self.rate * delta_time


class Building:
    def __init__(self, name, base_cost, resource_production, cost_multiplier=1.1):
        self.name = name
        self.base_cost = base_cost
        self.current_cost = base_cost.copy()
        self.resource_production = resource_production
        self.cost_multiplier = cost_multiplier
        self.count = 0  # Track how many buildings of this type exist

    def max_affordable(self, resources):
        """Calculate the maximum number of buildings that can be purchased."""
        max_count = float('inf')
        for res, amt in self.current_cost.items():
            if resources[res].amount < amt:
                return 0
            max_count = min(max_count, resources[res].amount // amt)
        return int(max_count)

    def build(self, resources, quantity=1):
        """Build the specified quantity of buildings if affordable."""
        for _ in range(quantity):
            if not self.can_build(resources, quantity=1):
                return False
            for res in self.current_cost:
                resources[res].amount -= self.current_cost[res]
            self.count += 1
            for res, rate in self.resource_production.items():
                resources[res].rate += rate
            self.increase_cost()
        return True

    def can_build(self, resources, quantity=1):
        """Check if the building can be built in the specified quantity."""
        return all(resources[res].amount >= self.current_cost[res] * quantity for res in self.current_cost)

    def increase_cost(self):
        """Increase the cost of the building after each purchase."""
        for res in self.current_cost:
            self.current_cost[res] = int(self.current_cost[res] * self.cost_multiplier)

    def to_dict(self):
        """Serialize the building to a dictionary."""
        return {
            "name": self.name,
            "current_cost": self.current_cost,
            "count": self.count
        }

    @staticmethod
    def from_dict(data, base_cost, resource_production, cost_multiplier):
        """Deserialize a building from a dictionary."""
        building = Building(data["name"], base_cost, resource_production, cost_multiplier)
        building.current_cost = data.get("current_cost", base_cost)
        building.count = data.get("count", 0)  # Default to 0 if "count" is missing
        return building


class Civilization:
    def __init__(self):
        self.age = "Caveman Age"
        self.resources = {
            "food": Resource("Food", amount=10, rate=1),
            "wood": Resource("Wood", amount=0, rate=0),
            "metal": Resource("Metal", amount=0, rate=0),
        }
        self.buildings = [
            Building("Hut", base_cost={"food": 10}, resource_production={"wood": 1}),
            Building("Farm", base_cost={"wood": 15}, resource_production={"food": 2}),
            Building("Mine", base_cost={"food": 20, "wood": 10}, resource_production={"metal": 1}),
        ]
        self.ages = ["Caveman Age", "Agricultural Age", "Industrial Age",
                     "Information Age", "Space Age", "Intergalactic Age"]
        self.age_requirements = self.initialize_age_requirements()

    def initialize_age_requirements(self):
        """Initialize exponentially increasing requirements for each age."""
        requirements = {
            "Agricultural Age": {"food": 50},
        }
        multiplier = 2  # Exponential scaling factor
        for i in range(2, len(self.ages)):
            prev_age = self.ages[i - 1]
            requirements[self.ages[i]] = {
                res: int(req * multiplier)
                for res, req in requirements[prev_age].items()
            }
            multiplier *= 1.5  # Gradually increase the scaling factor
        return requirements

    def can_advance_age(self):
        if self.age == self.ages[-1]:
            return False
        next_age = self.ages[self.ages.index(self.age) + 1]
        requirements = self.age_requirements[next_age]
        return all(self.resources[res].amount >= req for res, req in requirements.items())

    def get_next_age_requirements(self):
        if self.age == self.ages[-1]:
            return None
        next_age = self.ages[self.ages.index(self.age) + 1]
        return next_age, self.age_requirements[next_age]

    def advance_age(self):
        if self.can_advance_age():
            next_age = self.ages[self.ages.index(self.age) + 1]
            requirements = self.age_requirements[next_age]
            for res, req in requirements.items():
                self.resources[res].amount -= req
            self.age = next_age
            return True
        return False

    def tick(self, delta_time):
        for resource in self.resources.values():
            resource.generate(delta_time)

    def to_dict(self):
        """Serialize the civilization."""
        return {
            "age": self.age,
            "resources": {name: {"amount": int(res.amount), "rate": int(res.rate)} for name, res in self.resources.items()},
            "buildings": [building.to_dict() for building in self.buildings]
        }

    @staticmethod
    def from_dict(data):
        """Deserialize the civilization."""
        civ = Civilization()
        civ.age = data["age"]
        for name, res_data in data["resources"].items():
            civ.resources[name].amount = res_data["amount"]
            civ.resources[name].rate = res_data["rate"]

        # Load buildings with a fallback to default if "buildings" is missing
        buildings_data = data.get("buildings", [])
        for building_data, building_template in zip(buildings_data, civ.buildings):
            building_template.current_cost = building_data.get("current_cost", building_template.base_cost)
            building_template.count = building_data.get("count", 0)
        return civ


class Button:
    def __init__(self, text, x, y, width, height, color, action):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.action = action
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(x, y, width, height)

    def update_position(self, x, y):
        """Update the button's position dynamically."""
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, active=True):
        """Draw the button. Gray it out if inactive."""
        color = (150, 150, 150) if not active else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


class IdleGame:
    SAVE_FILE = "game_state.json"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Civilization Idle Game")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.running = True

        self.civ = self.load_game() or Civilization()

        self.messages = []
        self.buttons = []

        # Current purchase quantity (default is 1)
        self.purchase_quantity = 1

        # Create advance age button
        self.advance_age_button = Button(
            text="Advance Age",
            x=20, y=200, width=200, height=40,
            color=(200, 200, 200),
            action=self.advance_age
        )

        # Quantity selector buttons
        quantities = [1, 5, 10, 100, "Max"]
        self.quantity_buttons = []
        x_offset = 800
        for qty in quantities:
            button = Button(
                text=f"{qty}x",
                x=x_offset, y=20, width=60, height=40,
                color=(200, 200, 200),
                action=lambda q=qty: self.set_purchase_quantity(q)
            )
            self.quantity_buttons.append(button)
            x_offset += 70

        # Create buttons for buildings
        y_offset = 100
        for building in self.civ.buildings:
            button = Button(
                text=f"Build {building.name}",
                x=800, y=y_offset, width=200, height=40,
                color=(200, 200, 200),
                action=lambda b=building: self.build_building(b)
            )
            self.buttons.append(button)
            y_offset += 70

    def save_game(self):
        with open(self.SAVE_FILE, "w") as f:
            json.dump(self.civ.to_dict(), f)

    def load_game(self):
        if os.path.exists(self.SAVE_FILE):
            with open(self.SAVE_FILE, "r") as f:
                return Civilization.from_dict(json.load(f))
        return None

    def set_purchase_quantity(self, qty):
        """Set the number of buildings to buy."""
        self.purchase_quantity = float('inf') if qty == "Max" else qty
        self.messages.append(f"Purchase quantity set to {qty}.")

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.advance_age_button.handle_event(event)
            for button in self.buttons + self.quantity_buttons:
                button.handle_event(event)

    def update_button_positions(self):
        """Update button positions dynamically based on the window size."""
        window_width = self.screen.get_width()

        # Update quantity buttons
        x_offset = window_width - (len(self.quantity_buttons) * 70) - 20
        for button in self.quantity_buttons:
            button.update_position(x_offset, 20)
            x_offset += 70

        # Update building buttons
        x_offset = window_width - 220
        y_offset = 100
        for button in self.buttons:
            button.update_position(x_offset, y_offset)
            y_offset += 70

    def build_building(self, building):
        quantity = self.purchase_quantity if self.purchase_quantity != float('inf') else building.max_affordable(
            self.civ.resources)
        if quantity > 0 and building.build(self.civ.resources, quantity):
            self.messages.append(f"Built {quantity} {building.name}(s)!")
        else:
            self.messages.append(f"Cannot build {building.name}. Not enough resources!")

    def advance_age(self):
        if self.civ.advance_age():
            self.messages.append(f"Advanced to {self.civ.age}!")
        else:
            self.messages.append("Cannot advance age. Requirements not met.")

    def game_loop(self):
        while self.running:
            delta_time = self.clock.tick(30) / 1000.0  # Convert milliseconds to seconds
            self.handle_events()
            self.update_button_positions()

            self.civ.tick(delta_time)

            self.screen.fill((0, 0, 0))  # Clear screen

            # Draw Age
            self.draw_text(f"Age: {self.civ.age}", 20, 20)

            # Draw Resources
            y_offset = 80
            for res_name, res_obj in self.civ.resources.items():
                self.draw_text(f"{res_name.capitalize()}: {int(res_obj.amount)} (+{int(res_obj.rate)}/s)", 20, y_offset)
                y_offset += 40

            # Draw Advance Age Button and Next Age Requirements
            active = self.civ.can_advance_age()
            self.advance_age_button.draw(self.screen, active=active)
            next_age_data = self.civ.get_next_age_requirements()
            if next_age_data:
                next_age, reqs = next_age_data
                reqs_text = ", ".join(f"{res}: {amt}" for res, amt in reqs.items())
                self.draw_text(f"Requirements: {reqs_text}", 20, 250)

            # Draw Buttons and Building Info
            for button, building in zip(self.buttons, self.civ.buildings):
                active = building.can_build(self.civ.resources, quantity=self.purchase_quantity)
                button.draw(self.screen, active=active)
                self.draw_text(
                    f"Owned: {building.count} | Cost: {', '.join(f'{res}: {int(amt)}' for res, amt in building.current_cost.items())}",
                    button.rect.x - 500, button.rect.y + 10
                )

            pygame.display.flip()

        self.save_game()
        pygame.quit()


if __name__ == "__main__":
    game = IdleGame()
    game.game_loop()
