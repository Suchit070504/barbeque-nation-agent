import json

class StateMachine:
    def __init__(self):
        with open("state_machine/prompts/collect_city.json") as f:
            self.prompts = {"Collect_City": json.load(f)}
        with open("state_machine/transitions.json") as f:
            self.transitions = json.load(f)
        self.current_state = "Greeting"

    def get_prompt(self):
        return self.prompts.get(self.current_state, {}).get("instruction", "")

    def next(self, intent):
        for t in self.transitions:
            if t["current_state"] == self.current_state and t["intent"] == intent:
                self.current_state = t["next_state"]
                return self.get_prompt()
        return "Sorry, I didn’t understand that."
